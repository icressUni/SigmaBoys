from flask import Flask, render_template, request, jsonify
import os
import base64
import uuid
import json
import re
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import cv2
import numpy as np
import imgaug.augmenters as iaa
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import tempfile
import shutil

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_URL = "postgresql://alumnos_db_owner:npg_S7BvNrnaRLy5@ep-rapid-glitter-aaxbrr0d-pooler.westus3.azure.neon.tech/alumnos_db?sslmode=require&channel_binding=require"

# Configuración de Azure Blob Storage
storage_account_name = "rostros"
storage_account_key = "uAQmF0ywSUJrO82FnmikIBkxZp8HOW+Uk9nN4tvYN7iEebOU22TwGvqeXBmetS9K6Aykr01gtWu/+ASt4Ww6og=="
connection_string = "DefaultEndpointsProtocol=https;AccountName=rostros;AccountKey=P8cGoet0uIRcDvoO9SkOtUc4paCWX1KYZsR8evoS0QlODr6rwOF3qKgnNm0A5784ZoBxjckClvsq+AStCBK3wA==;EndpointSuffix=core.windows.net"
container_name = "public"



def upload_blob(file_path, blob_name):
    """Sube un archivo al Azure Blob Storage"""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        print(f"Blob '{blob_name}' uploaded successfully to container '{container_name}'.")
        return True
    except Exception as e:
        print(f"Error uploading blob '{blob_name}': {e}")
        return False

def upload_folder_to_blob(local_folder_path, blob_folder_name):
    """Sube una carpeta completa al Azure Blob Storage"""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        uploaded_files = []
        
        for root, dirs, files in os.walk(local_folder_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                # Crear la ruta del blob manteniendo la estructura de carpetas
                relative_path = os.path.relpath(local_file_path, local_folder_path)
                blob_name = f"{blob_folder_name}/{relative_path}".replace("\\", "/")
                
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
                
                with open(local_file_path, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)
                
                uploaded_files.append(blob_name)
                print(f"Archivo '{file}' subido como blob '{blob_name}'")
        
        print(f"Carpeta '{local_folder_path}' subida exitosamente como '{blob_folder_name}' con {len(uploaded_files)} archivos")
        return True, uploaded_files
    except Exception as e:
        print(f"Error subiendo carpeta al blob: {e}")
        return False, []

def validate_email(email):
    """Valida el formato del email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_db_connection():
    """Establece conexión con la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def email_exists(correo):
    """Verifica si el correo electrónico ya existe en la base de datos"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM alumnos WHERE correo = %s", (correo.lower(),))
        count = cursor.fetchone()[0]
        return count > 0
    except psycopg2.Error as e:
        print(f"Error verificando correo: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def insert_student(nombre, apellido, correo, especialidad, image_filename):
    """Inserta un nuevo estudiante en la base de datos"""
    conn = get_db_connection()
    if not conn:
        return False, None
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alumnos (nombre, apellido, correo, especialidad)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (nombre.strip(), apellido.strip(), correo.lower().strip(), especialidad.strip()))
        
        student_id = cursor.fetchone()[0]
        conn.commit()
        return True, str(student_id)
    except psycopg2.Error as e:
        print(f"Error insertando estudiante: {e}")
        conn.rollback()
        return False, None
    finally:
        cursor.close()
        conn.close()

def augment_image(image_path, output_dir, num_augmented=10):
    """
    Genera imágenes aumentadas usando data augmentation
    """
    try:
        # Cargar la imagen
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: No se pudo cargar la imagen {image_path}")
            return False
        
        # Crear el directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)
        
        # Definir los augmenters
        augmenters = iaa.Sequential([
            iaa.Fliplr(0.5),  # Reflejo horizontal con 50% de probabilidad
            iaa.Affine(rotate=(-20, 20)),  # Rotación entre -20 y 20 grados
            iaa.Affine(translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)}), # Traslación
            iaa.Multiply((0.8, 1.2)),  # Variación de brillo
            iaa.GaussianBlur(sigma=(0, 1.5))  # Desenfoque ligero
            
            #TRANSFORMACIONES EXTRA
            #iaa.AddToHueAndSaturation(value=(-30, 30)),  # Modificar matiz
            #iaa.AdditiveGaussianNoise(scale=(0, 0.1*255)),  # Agregar ruido gaussiano
            #iaa.PiecewiseAffine(scale=(0.01, 0.05))  # Deformación tipo malla
        ])
        
        # Generar las imágenes aumentadas
        for i in range(num_augmented):
            augmented_image = augmenters.augment_image(image)
            output_path = os.path.join(output_dir, f"augmented_{i}.jpg")
            cv2.imwrite(output_path, augmented_image)
        
        print(f"Generadas {num_augmented} imágenes aumentadas en {output_dir}")
        return True
        
    except Exception as e:
        print(f"Error en data augmentation: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_photo', methods=['POST'])
def save_photo():
    data = request.json
    image_data = data.get('imageData')
    nombre = data.get('nombre', '').strip()
    apellido = data.get('apellido', '').strip()
    correo = data.get('correo', '').strip().lower()
    especialidad = data.get('especialidad', '').strip()

    print(f"Datos recibidos: nombre={nombre}, apellido={apellido}, correo={correo}, especialidad={especialidad}")
    print(f"Imagen recibida: {'Sí' if image_data else 'No'}")

    # Validar campos de texto primero
    if not nombre:
        return jsonify({'status': 'error', 'message': 'El nombre es requerido'}), 400
    if not apellido:
        return jsonify({'status': 'error', 'message': 'El apellido es requerido'}), 400
    if not correo:
        return jsonify({'status': 'error', 'message': 'El correo es requerido'}), 400
    if not especialidad:
        return jsonify({'status': 'error', 'message': 'La especialidad es requerida'}), 400
    if not image_data:
        return jsonify({'status': 'error', 'message': 'La imagen es requerida'}), 400

    # Validar formato del correo
    if not validate_email(correo):
        return jsonify({'status': 'error', 'message': 'El formato del correo electrónico no es válido'}), 400

    # PRIMERO: Verificar si el correo ya existe en la base de datos
    print(f"Verificando si el correo {correo} ya existe...")
    if email_exists(correo):
        return jsonify({'status': 'error', 'message': 'El correo electrónico ya está registrado'}), 409

    # Generar un ID único para el nombre de la imagen
    image_uuid = str(uuid.uuid4())

    print(f"Correo no existe, procediendo con el registro...")
    print(f"UUID generado: {image_uuid}")

    # Crear directorio temporal para procesar las imágenes
    temp_dir = tempfile.mkdtemp()
    temp_image_path = None
    temp_augmented_folder = None

    try:
        # Decodificar la imagen base64
        print("Decodificando imagen...")
        header, encoded = image_data.split(',', 1)
        ext = header.split('/')[1].split(';')[0]  # png, jpeg, etc.
        img = base64.b64decode(encoded)

        # Guardar la imagen original temporalmente
        image_filename = f"original.{ext}"
        temp_image_path = os.path.join(temp_dir, image_filename)
        with open(temp_image_path, 'wb') as f:
            f.write(img)
        print(f"Imagen original guardada temporalmente en: {temp_image_path}")

        # Crear carpeta temporal para las imágenes aumentadas
        temp_augmented_folder = os.path.join(temp_dir, "augmented")
        print(f"Creando carpeta temporal para imágenes aumentadas: {temp_augmented_folder}")
        
        # Generar las imágenes aumentadas
        print("Iniciando data augmentation...")
        augmentation_success = augment_image(temp_image_path, temp_augmented_folder, num_augmented=10)
        
        if augmentation_success:
            print("Data augmentation completado exitosamente")
        else:
            print("Error en data augmentation")
            return jsonify({'status': 'error', 'message': 'Error en el procesamiento de imágenes'}), 500

        # Insertar SOLO los datos del estudiante en la base de datos (sin la imagen)
        print("Insertando datos en la base de datos...")
        success, student_id = insert_student(nombre, apellido, correo, especialidad, f"{image_uuid}.{ext}")
        
        if success and student_id:
            print(f"Estudiante registrado exitosamente con ID: {student_id}")
            
            # SUBIR LA IMAGEN ORIGINAL AL BLOB
            print("Subiendo imagen original al Azure Blob Storage...")
            blob_original_name = f"{student_id}/original.{ext}"
            upload_success_original = upload_blob(temp_image_path, blob_original_name)
            
            if not upload_success_original:
                print("Error subiendo imagen original al blob")
                # Aunque falle la subida al blob, continuamos con el proceso
            else:
                print(f"Imagen original subida exitosamente al blob como: {blob_original_name}")
            
            # SUBIR LAS IMÁGENES AUMENTADAS AL BLOB
            print("Subiendo imágenes aumentadas al Azure Blob Storage...")
            blob_folder_name = f"{student_id}/augmented"
            upload_success_augmented, uploaded_files = upload_folder_to_blob(temp_augmented_folder, blob_folder_name)
            
            if not upload_success_augmented:
                print("Error subiendo imágenes aumentadas al blob")
                # Aunque falle la subida al blob, continuamos con el proceso
            else:
                print(f"Imágenes aumentadas subidas exitosamente al blob en la carpeta: {blob_folder_name}")
            
            return jsonify({
                'status': 'success', 
                'id': student_id,
                'message': f'Estudiante {nombre} {apellido} registrado exitosamente',
                'blob_original_path': blob_original_name,
                'blob_augmented_folder': blob_folder_name,
                'augmentation_success': augmentation_success,
                'blob_upload_success': upload_success_original and upload_success_augmented,
                'uploaded_files_count': len(uploaded_files) if uploaded_files else 0
            })
        else:
            print("Error al insertar en la base de datos")
            return jsonify({'status': 'error', 'message': 'Error al guardar en la base de datos'}), 500

    except Exception as e:
        print(f"Error procesando la foto: {e}")
        return jsonify({'status': 'error', 'message': f'Error procesando la imagen: {str(e)}'}), 500
    
    finally:
        # Limpiar archivos temporales
        try:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                print("Archivos temporales limpiados")
        except Exception as e:
            print(f"Error limpiando archivos temporales: {e}")

@app.route('/get_metadata', methods=['GET'])
def get_metadata():
    """Endpoint para obtener todos los metadatos desde la base de datos"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'status': 'error', 'message': 'Error de conexión a la base de datos'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id, nombre, apellido, correo, especialidad FROM alumnos ORDER BY nombre, apellido")
        students = cursor.fetchall()
        
        # Convertir a lista de diccionarios para JSON
        students_list = []
        for student in students:
            student_dict = dict(student)
            # Convertir UUID a string
            if 'id' in student_dict:
                student_dict['id'] = str(student_dict['id'])
            students_list.append(student_dict)
        
        return jsonify({'status': 'success', 'data': students_list, 'count': len(students_list)})
    except psycopg2.Error as e:
        print(f"Error obteniendo metadatos: {e}")
        return jsonify({'status': 'error', 'message': 'Error al obtener los datos'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/check_email', methods=['POST'])
def check_email():
    """Endpoint para verificar si un correo ya existe (útil para validación en tiempo real)"""
    data = request.json
    correo = data.get('correo', '').strip().lower()
    
    if not correo:
        return jsonify({'status': 'error', 'message': 'Correo requerido'}), 400
    
    if not validate_email(correo):
        return jsonify({'status': 'error', 'message': 'Formato de correo inválido'}), 400
    
    exists = email_exists(correo)
    return jsonify({'status': 'success', 'exists': exists})

@app.route('/get_student/<student_id>', methods=['GET'])
def get_student(student_id):
    """Endpoint para obtener un estudiante específico por ID"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'status': 'error', 'message': 'Error de conexión a la base de datos'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id, nombre, apellido, correo, especialidad FROM alumnos WHERE id = %s", (student_id,))
        student = cursor.fetchone()
        
        if student:
            student_dict = dict(student)
            student_dict['id'] = str(student_dict['id'])
            return jsonify({'status': 'success', 'data': student_dict})
        else:
            return jsonify({'status': 'error', 'message': 'Estudiante no encontrado'}), 404
            
    except psycopg2.Error as e:
        print(f"Error obteniendo estudiante: {e}")
        return jsonify({'status': 'error', 'message': 'Error al obtener el estudiante'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar el estado de la aplicación y la base de datos"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            
            # También verificar conexión con Azure Blob Storage
            try:
                blob_service_client = BlobServiceClient.from_connection_string(connection_string)
                container_client = blob_service_client.get_container_client(container_name)
                container_client.get_container_properties()
                blob_status = "OK"
            except Exception as e:
                blob_status = f"Error: {str(e)}"
            
            return jsonify({
                'status': 'success', 
                'message': 'Aplicación funcionando correctamente',
                'database': 'OK',
                'blob_storage': blob_status
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Error en la base de datos: {str(e)}'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'No se puede conectar a la base de datos'}), 500

# Por esto:
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)