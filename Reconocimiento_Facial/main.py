# Instalación previa necesaria:
# pip install face_recognition opencv-python numpy psycopg2-binary

import face_recognition
import cv2
import numpy as np
import os
import pickle
import json
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'ep-rapid-glitter-aaxbrr0d-pooler.westus3.azure.neon.tech',
    'database': 'alumnos_db',
    'user': 'alumnos_db_owner',
    'password': 'npg_S7BvNrnaRLy5',
    'sslmode': 'require'
}

def conectar_db():
    """
    Establece conexión con la base de datos PostgreSQL
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def obtener_alumno_id(nombre):
    """
    Obtiene el ID del alumno basado en su nombre (busca en nombre y apellido)
    """
    conn = conectar_db()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        # Buscar por nombre completo o por coincidencia en nombre o apellido
        cursor.execute("""
            SELECT id FROM alumnos 
            WHERE LOWER(CONCAT(nombre, ' ', apellido)) LIKE LOWER(%s)
            OR LOWER(nombre) LIKE LOWER(%s)
            OR LOWER(apellido) LIKE LOWER(%s)
            LIMIT 1
        """, (f'%{nombre}%', f'%{nombre}%', f'%{nombre}%'))
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado:
            return resultado['id']
        else:
            print(f"Alumno '{nombre}' no encontrado en la base de datos")
            return None
    except Exception as e:
        print(f"Error al buscar alumno: {e}")
        conn.close()
        return None

def gestionar_asistencia(alumno_id):
    """
    Gestiona el registro de asistencia (entrada/salida) en la base de datos
    """
    conn = conectar_db()
    if not conn:
        return False, "Error de conexión a la base de datos"
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        timestamp_actual = datetime.now()
        
        # Buscar si existe un registro de asistencia incompleto (solo entrada) para hoy
        cursor.execute("""
            SELECT id, entrada, salida 
            FROM asistencias 
            WHERE alumnos_id = %s 
            AND DATE(entrada) = CURRENT_DATE 
            AND salida IS NULL
            ORDER BY entrada DESC 
            LIMIT 1
        """, (alumno_id,))
        
        registro_incompleto = cursor.fetchone()
        
        if registro_incompleto:
            # Existe un registro con solo entrada, marcar salida
            cursor.execute("""
                UPDATE asistencias 
                SET salida = %s 
                WHERE id = %s
            """, (timestamp_actual, registro_incompleto['id']))
            
            conn.commit()
            conn.close()
            return True, f"Salida registrada exitosamente a las {timestamp_actual.strftime('%H:%M:%S')}"
        
        else:
            # No hay registro incompleto, crear nuevo registro de entrada
            cursor.execute("""
                INSERT INTO asistencias (alumnos_id, entrada) 
                VALUES (%s, %s) 
                RETURNING id
            """, (alumno_id, timestamp_actual))
            
            nuevo_id = cursor.fetchone()['id']
            conn.commit()
            conn.close()
            return True, f"Entrada registrada exitosamente a las {timestamp_actual.strftime('%H:%M:%S')} (ID: {nuevo_id})"
    
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al registrar asistencia: {e}"

def crear_base_de_datos_rostros(directorio_personas):
    """
    Crea una base de datos de rostros conocidos a partir de imágenes en un directorio.
    Cada subdirectorio debe tener el nombre de la persona y contener sus fotos.
    """
    rostros_conocidos = []
    nombres_conocidos = []
    
    # Recorrer cada subdirectorio (persona)
    for persona in os.listdir(directorio_personas):
        ruta_persona = os.path.join(directorio_personas, persona)
        if os.path.isdir(ruta_persona):
            # Recorrer cada imagen en el subdirectorio
            for imagen_archivo in os.listdir(ruta_persona):
                if imagen_archivo.endswith(('.jpg', '.jpeg', '.png')):
                    ruta_completa = os.path.join(ruta_persona, imagen_archivo)
                    try:
                        # Cargar la imagen y encontrar codificación facial
                        imagen = face_recognition.load_image_file(ruta_completa)
                        codificaciones = face_recognition.face_encodings(imagen)
                        
                        # Si se encontró un rostro, agregarlo a la base de datos
                        if codificaciones:
                            rostros_conocidos.append(codificaciones[0])
                            nombres_conocidos.append(persona)
                            print(f"Rostro de {persona} agregado a la base de datos")
                        else:
                            print(f"No se encontró ningún rostro en {ruta_completa}")
                    except Exception as e:
                        print(f"Error al procesar {ruta_completa}: {str(e)}")
    
    return rostros_conocidos, nombres_conocidos

def cargar_modelo(ruta_modelo):
    """
    Carga el modelo de rostros conocidos desde un archivo.
    """
    if not os.path.exists(ruta_modelo):
        print(f"El archivo de modelo {ruta_modelo} no existe. Crea el modelo primero.")
        return [], []
    
    with open(ruta_modelo, 'rb') as modelo_file:
        data = pickle.load(modelo_file)
        return data["rostros"], data["nombres"]

def reconocimiento_imagen(ruta_imagen, rostros_conocidos, nombres_conocidos):
    """
    Reconoce rostros en una imagen y los identifica contra la base de datos.
    """
    # Cargar la imagen
    imagen = face_recognition.load_image_file(ruta_imagen)
    # Convertir a RGB (para OpenCV)
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    
    # Encontrar todos los rostros en la imagen
    ubicaciones_rostros = face_recognition.face_locations(imagen)
    codificaciones_rostros = face_recognition.face_encodings(imagen, ubicaciones_rostros)
    
    if not codificaciones_rostros:
        print("No se detectaron rostros. Intenta mejorar la iluminación o la calidad de la imagen.")
    
    # Mostrar resultados
    for (top, right, bottom, left), codificacion_rostro in zip(ubicaciones_rostros, codificaciones_rostros):
        coincidencias = face_recognition.compare_faces(rostros_conocidos, codificacion_rostro, tolerance=0.7)
        nombre = "Desconocido"
        distancias_faciales = face_recognition.face_distance(rostros_conocidos, codificacion_rostro)
        mejor_coincidencia = np.argmin(distancias_faciales) if len(distancias_faciales) > 0 else -1

        # Solo mostrar el nombre, sin la distancia
        if mejor_coincidencia >= 0 and coincidencias[mejor_coincidencia]:
            nombre = nombres_conocidos[mejor_coincidencia]
        elif mejor_coincidencia >= 0 and distancias_faciales[mejor_coincidencia] < 0.6:
            nombre = f"¿Quizás: {nombres_conocidos[mejor_coincidencia]}?"
        
        # Dibujar un rectángulo alrededor del rostro
        cv2.rectangle(imagen_rgb, (left, top), (right, bottom), (0, 255, 0), 2)
        
        # Dibujar una etiqueta con el nombre debajo del rostro
        cv2.rectangle(imagen_rgb, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(imagen_rgb, nombre, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)
    
    # Mostrar la imagen resultante
    cv2.imshow('Reconocimiento Facial', imagen_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def reconocimiento_camara(rostros_conocidos, nombres_conocidos):
    """
    Realiza reconocimiento facial usando la cámara web con protección contra registros duplicados.
    """
    # Iniciar la cámara web
    captura = cv2.VideoCapture(0)
    
    if not captura.isOpened():
        print("No se pudo acceder a la cámara")
        return
    
    print("Presiona 'q' para salir")
    print("Presiona 'r' para registrar asistencia de la persona identificada")
    print("=" * 60)

    rostro_seguido = None
    ubicacion_seguida = None
    tiempo_espera = 0
    ultimo_registro = 0  # Timestamp del último registro para evitar duplicados
    COOLDOWN_REGISTRO = 3  # Segundos de espera entre registros
    
    while True:
        ret, frame = captura.read()
        if not ret:
            break
            
        # Redimensionar el frame para un procesamiento más rápido
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        if rostro_seguido is None and tiempo_espera == 0:
            # Encontrar rostros en el frame actual
            ubicaciones_rostros = face_recognition.face_locations(rgb_small_frame)
            codificaciones_rostros = face_recognition.face_encodings(rgb_small_frame, ubicaciones_rostros)
            
            for ubicacion, codificacion_rostro in zip(ubicaciones_rostros, codificaciones_rostros):
                coincidencias = face_recognition.compare_faces(rostros_conocidos, codificacion_rostro, tolerance=0.7)
                nombre = "Desconocido"
                distancias_faciales = face_recognition.face_distance(rostros_conocidos, codificacion_rostro)
                mejor_coincidencia = np.argmin(distancias_faciales) if len(distancias_faciales) > 0 else -1

                if mejor_coincidencia >= 0 and coincidencias[mejor_coincidencia]:
                    nombre = nombres_conocidos[mejor_coincidencia]
                elif mejor_coincidencia >= 0 and distancias_faciales[mejor_coincidencia] < 0.6:
                    nombre = f"¿Quizás: {nombres_conocidos[mejor_coincidencia]}?"
                
                if nombre != "Desconocido":
                    rostro_seguido = nombre
                    ubicacion_seguida = ubicacion
                    print(f"Rostro identificado: {nombre}")
                    break
                else:
                    # Seguir al rostro desconocido hasta que salga del cuadro
                    rostro_seguido = "Desconocido"
                    ubicacion_seguida = ubicacion
                    print("Rostro desconocido detectado")
                    break
        elif tiempo_espera > 0:
            tiempo_espera -= 1
        else:
            # Actualizar la ubicación del rostro seguido
            ubicaciones_rostros = face_recognition.face_locations(rgb_small_frame)
            if ubicaciones_rostros:
                # Buscar la ubicación más cercana a la anterior
                if ubicacion_seguida is not None:
                    # Calcular la distancia entre ubicaciones
                    distancias = [np.linalg.norm(np.array(ubicacion_seguida) - np.array(u)) for u in ubicaciones_rostros]
                    idx_min = np.argmin(distancias)
                    ubicacion_seguida = ubicaciones_rostros[idx_min]
                else:
                    ubicacion_seguida = ubicaciones_rostros[0]
            else:
                # Si el rostro sale del cuadro, reiniciar el seguimiento
                rostro_seguido = None
                ubicacion_seguida = None
        
        if rostro_seguido and ubicacion_seguida:
            # Escalar de vuelta las ubicaciones al tamaño original
            top, right, bottom, left = [v * 4 for v in ubicacion_seguida]
            
            # Dibujar un recuadro alrededor del rostro seguido
            color = (0, 255, 0) if rostro_seguido != "Desconocido" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Dibujar una etiqueta con el nombre
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, rostro_seguido, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)
            
            # Mostrar tiempo restante de cooldown si aplica
            tiempo_actual = time.time()
            if (tiempo_actual - ultimo_registro) < COOLDOWN_REGISTRO:
                tiempo_restante = COOLDOWN_REGISTRO - (tiempo_actual - ultimo_registro)
                cv2.putText(frame, f"Espera: {tiempo_restante:.1f}s", (10, 30), font, 0.7, (0, 255, 255), 2)
        
        # Mostrar el frame resultante
        cv2.imshow('Reconocimiento Facial en Vivo', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r') and rostro_seguido and rostro_seguido != "Desconocido":
            # Verificar cooldown para evitar registros duplicados
            tiempo_actual = time.time()
            if (tiempo_actual - ultimo_registro) < COOLDOWN_REGISTRO:
                tiempo_restante = COOLDOWN_REGISTRO - (tiempo_actual - ultimo_registro)
                print(f"⚠️  Espera {tiempo_restante:.1f} segundos antes del próximo registro")
                continue
            
            # Limpiar el nombre de caracteres especiales si los hay
            nombre_limpio = rostro_seguido.split("(")[0].strip() if "(" in rostro_seguido else rostro_seguido
            
            print(f"Procesando registro para: {nombre_limpio}")
            
            # Obtener ID del alumno
            alumno_id = obtener_alumno_id(nombre_limpio)
            
            if alumno_id is None:
                print(f"❌ Error: Alumno '{nombre_limpio}' no encontrado en la base de datos")
                print("   Verifica que el nombre coincida exactamente con la base de datos")
                ultimo_registro = tiempo_actual  # Actualizar para evitar spam
                continue
            
            # Registrar asistencia
            exito, mensaje = gestionar_asistencia(alumno_id)
            
            if exito:
                print(f"✅ {mensaje}")
            else:
                print(f"❌ {mensaje}")
                print("   Intenta registrar nuevamente")
            
            ultimo_registro = tiempo_actual
            print("-" * 60)
    
    # Liberar recursos
    captura.release()
    cv2.destroyAllWindows()

# Ejemplo de uso:
if __name__ == "__main__":
    # Ruta del archivo de modelo
    ruta_modelo = "./model/modelo_rostros.pkl"
    
    # Cargar el modelo
    rostros_conocidos, nombres_conocidos = cargar_modelo(ruta_modelo)
    
    # Verificar si el modelo contiene datos
    if not rostros_conocidos or not nombres_conocidos:
        print("El modelo está vacío o no contiene datos válidos. Verifica que el archivo modelo_rostros.pkl fue generado correctamente.")
        print(f"Rostros conocidos: {len(rostros_conocidos)}, Nombres conocidos: {len(nombres_conocidos)}")
    else:
        print(f"Modelo cargado correctamente. Rostros conocidos: {len(rostros_conocidos)}, Nombres conocidos: {len(nombres_conocidos)}")
        print("Verificando conexión a la base de datos...")
        
        # Probar conexión a la base de datos
        conn_test = conectar_db()
        if conn_test:
            print("✅ Conexión a PostgreSQL establecida correctamente")
            conn_test.close()
            
            # Iniciar reconocimiento en tiempo real
            reconocimiento_camara(rostros_conocidos, nombres_conocidos)
        else:
            print("❌ Error: No se pudo conectar a la base de datos PostgreSQL")
            print("   Verifica la configuración de conexión")