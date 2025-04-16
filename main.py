# Instalación previa necesaria:
# pip install face_recognition opencv-python numpy

import face_recognition
import cv2
import numpy as np
import os
import pickle

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
    
    # Mostrar resultados
    for (top, right, bottom, left), codificacion_rostro in zip(ubicaciones_rostros, codificaciones_rostros):
        # Comparar el rostro con nuestra base de datos
        coincidencias = face_recognition.compare_faces(rostros_conocidos, codificacion_rostro, tolerance=0.4)  # Aumentar exigencia
        nombre = "Desconocido"
        
        # Usar la distancia facial para encontrar la mejor coincidencia
        distancias_faciales = face_recognition.face_distance(rostros_conocidos, codificacion_rostro)
        mejor_coincidencia = np.argmin(distancias_faciales) if len(distancias_faciales) > 0 else -1
        
        if mejor_coincidencia >= 0 and coincidencias[mejor_coincidencia]:
            nombre = nombres_conocidos[mejor_coincidencia]
        
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
    Realiza reconocimiento facial usando la cámara web.
    """
    # Iniciar la cámara web
    captura = cv2.VideoCapture(0)
    
    if not captura.isOpened():
        print("No se pudo acceder a la cámara")
        return
    
    print("Presiona 'q' para salir")
    
    rostro_seguido = None
    ubicacion_seguida = None
    tiempo_espera = 0
    
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
                # Comparar con rostros conocidos
                coincidencias = face_recognition.compare_faces(rostros_conocidos, codificacion_rostro, tolerance=0.4)
                nombre = "Desconocido"
                
                # Encontrar la mejor coincidencia
                distancias_faciales = face_recognition.face_distance(rostros_conocidos, codificacion_rostro)
                mejor_coincidencia = np.argmin(distancias_faciales) if len(distancias_faciales) > 0 else -1
                
                if mejor_coincidencia >= 0 and coincidencias[mejor_coincidencia]:
                    nombre = nombres_conocidos[mejor_coincidencia]
                
                if nombre != "Desconocido":
                    rostro_seguido = nombre
                    ubicacion_seguida = ubicacion
                    print(f"Rostro identificado: {nombre}")
                    break
                else:
                    # Dibujar una caja con "Desconocido"
                    top, right, bottom, left = [v * 4 for v in ubicacion]
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, "Desconocido", (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)
                    tiempo_espera = 90  # 3 segundos a 30 FPS
        elif tiempo_espera > 0:
            tiempo_espera -= 1
        else:
            # Actualizar la ubicación del rostro seguido
            ubicaciones_rostros = face_recognition.face_locations(rgb_small_frame)
            if ubicaciones_rostros:
                ubicacion_seguida = ubicaciones_rostros[0]
            else:
                # Si el rostro sale del cuadro, reiniciar el seguimiento
                rostro_seguido = None
                ubicacion_seguida = None
        
        if rostro_seguido and ubicacion_seguida:
            # Escalar de vuelta las ubicaciones al tamaño original
            top, right, bottom, left = [v * 4 for v in ubicacion_seguida]
            
            # Dibujar un recuadro alrededor del rostro seguido
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            
            # Dibujar una etiqueta con el nombre
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, rostro_seguido, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)
        
        # Mostrar el frame resultante
        cv2.imshow('Reconocimiento Facial en Vivo', frame)
        
        # Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Liberar recursos
    captura.release()
    cv2.destroyAllWindows()

# Ejemplo de uso:
if __name__ == "__main__":
    # Ruta del archivo de modelo
    ruta_modelo = "./modelo_rostros.pkl"
    
    # Cargar el modelo
    rostros_conocidos, nombres_conocidos = cargar_modelo(ruta_modelo)
    
    # Verificar si el modelo contiene datos
    if not rostros_conocidos or not nombres_conocidos:
        print("El modelo está vacío o no contiene datos válidos. Verifica que el archivo modelo_rostros.pkl fue generado correctamente.")
        print(f"Rostros conocidos: {len(rostros_conocidos)}, Nombres conocidos: {len(nombres_conocidos)}")
    else:
        print(f"Modelo cargado correctamente. Rostros conocidos: {len(rostros_conocidos)}, Nombres conocidos: {len(nombres_conocidos)}")
        
        # 3. Para reconocimiento en una imagen:
        # reconocimiento_imagen("ruta_a_la_imagen.jpg", rostros_conocidos, nombres_conocidos)
        
        # 4. Para reconocimiento en tiempo real con la cámara:
        reconocimiento_camara(rostros_conocidos, nombres_conocidos)