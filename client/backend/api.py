# api.py - API de reconocimiento facial con Flask
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import face_recognition
import cv2
import numpy as np
import os
import pickle
import base64
from io import BytesIO
import tempfile
import uuid

app = Flask(__name__)
CORS(app)  # Permite solicitudes de origen cruzado (CORS)

# Cargar el modelo de rostros conocidos
def cargar_modelo(ruta_modelo="./modelo_rostros.pkl"):
    """
    Carga el modelo de rostros conocidos desde un archivo.
    """
    if not os.path.exists(ruta_modelo):
        print(f"El archivo de modelo {ruta_modelo} no existe.")
        return [], []
    
    with open(ruta_modelo, 'rb') as modelo_file:
        data = pickle.load(modelo_file)
        return data["rostros"], data["nombres"]

# Punto de entrada para verificar que la API esté funcionando
@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "OK", "message": "API de reconocimiento facial funcionando correctamente"})

# Endpoint para reconocer rostros en una imagen subida
@app.route('/api/reconocer', methods=['POST'])
def reconocer_imagen():
    # Verificar si se envió una imagen
    if 'imagen' not in request.files:
        return jsonify({"error": "No se envió ninguna imagen"}), 400
    
    # Obtener la imagen y guardarla temporalmente
    archivo = request.files['imagen']
    temp_imagen = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    archivo.save(temp_imagen.name)
    temp_imagen.close()
    
    # Cargar el modelo
    rostros_conocidos, nombres_conocidos = cargar_modelo()
    
    if not rostros_conocidos or not nombres_conocidos:
        os.unlink(temp_imagen.name)
        return jsonify({"error": "El modelo de rostros no contiene datos"}), 500
    
    try:
        # Cargar la imagen
        imagen = face_recognition.load_image_file(temp_imagen.name)
        # Convertir a RGB
        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        
        # Encontrar rostros en la imagen
        ubicaciones_rostros = face_recognition.face_locations(imagen)
        codificaciones_rostros = face_recognition.face_encodings(imagen, ubicaciones_rostros)
        
        resultados = []
        
        for (top, right, bottom, left), codificacion_rostro in zip(ubicaciones_rostros, codificaciones_rostros):
            # Comparar con rostros conocidos
            coincidencias = face_recognition.compare_faces(rostros_conocidos, codificacion_rostro, tolerance=0.4)
            nombre = "Desconocido"
            
            # Encontrar la mejor coincidencia
            distancias_faciales = face_recognition.face_distance(rostros_conocidos, codificacion_rostro)
            mejor_coincidencia = np.argmin(distancias_faciales) if len(distancias_faciales) > 0 else -1
            
            if mejor_coincidencia >= 0 and coincidencias[mejor_coincidencia]:
                nombre = nombres_conocidos[mejor_coincidencia]
                confianza = float(1 - distancias_faciales[mejor_coincidencia])
            else:
                confianza = 0.0
            
            # Dibujar un rectángulo
            cv2.rectangle(imagen_rgb, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(imagen_rgb, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(imagen_rgb, nombre, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)
            
            resultados.append({
                "nombre": nombre,
                "confianza": round(confianza * 100, 2),
                "ubicacion": {
                    "top": top,
                    "right": right,
                    "bottom": bottom,
                    "left": left
                }
            })
        
        # Guardar la imagen procesada
        resultado_imagen_path = f"./temp/resultado_{uuid.uuid4()}.jpg"
        os.makedirs(os.path.dirname(resultado_imagen_path), exist_ok=True)
        cv2.imwrite(resultado_imagen_path, cv2.cvtColor(imagen_rgb, cv2.COLOR_RGB2BGR))
        
        # Codificar la imagen como base64 para enviar en la respuesta
        _, buffer = cv2.imencode('.jpg', cv2.cvtColor(imagen_rgb, cv2.COLOR_RGB2BGR))
        imagen_b64 = base64.b64encode(buffer).decode('utf-8')
        
        # Limpiar archivos temporales
        os.unlink(temp_imagen.name)
        
        return jsonify({
            "resultados": resultados,
            "imagen_procesada": imagen_b64,
            "imagen_path": resultado_imagen_path,
            "total_rostros": len(resultados)
        })
        
    except Exception as e:
        # Limpiar archivos temporales en caso de error
        os.unlink(temp_imagen.name)
        return jsonify({"error": str(e)}), 500

# Endpoint para obtener una imagen procesada
@app.route('/api/imagen/<path:imagen_path>', methods=['GET'])
def obtener_imagen(imagen_path):
    ruta_completa = f"./{imagen_path}"
    if os.path.exists(ruta_completa):
        return send_file(ruta_completa)
    else:
        return jsonify({"error": "Imagen no encontrada"}), 404

# Endpoint para crear o actualizar el modelo de rostros
@app.route('/api/crear-modelo', methods=['POST'])
def crear_modelo_api():
    if 'directorio' not in request.form:
        return jsonify({"error": "No se especificó un directorio"}), 400
    
    directorio = request.form['directorio']
    if not os.path.exists(directorio) or not os.path.isdir(directorio):
        return jsonify({"error": f"El directorio {directorio} no existe"}), 400
    
    try:
        rostros_conocidos = []
        nombres_conocidos = []
        
        # Recorrer cada subdirectorio (persona)
        for persona in os.listdir(directorio):
            ruta_persona = os.path.join(directorio, persona)
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
                        except Exception as e:
                            print(f"Error al procesar {ruta_completa}: {str(e)}")
        
        # Guardar el modelo
        ruta_modelo = "./modelo_rostros.pkl"
        with open(ruta_modelo, 'wb') as modelo_file:
            pickle.dump({"rostros": rostros_conocidos, "nombres": nombres_conocidos}, modelo_file)
        
        return jsonify({
            "mensaje": "Modelo creado correctamente",
            "rostros_registrados": len(rostros_conocidos),
            "personas_registradas": len(set(nombres_conocidos))
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)