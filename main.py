# Instalación previa necesaria:
# pip install face_recognition opencv-python numpy

import face_recognition
import cv2
import numpy as np
import os

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
        coincidencias = face_recognition.compare_faces(rostros_conocidos, codificacion_rostro)
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
    
    while True:
        ret, frame = captura.read()
        if not ret:
            break
            
        # Redimensionar el frame para un procesamiento más rápido
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Encontrar rostros en el frame actual
        ubicaciones_rostros = face_recognition.face_locations(rgb_small_frame)
        codificaciones_rostros = face_recognition.face_encodings(rgb_small_frame, ubicaciones_rostros)
        
        nombres_rostros = []
        
        for codificacion_rostro in codificaciones_rostros:
            # Comparar con rostros conocidos
            coincidencias = face_recognition.compare_faces(rostros_conocidos, codificacion_rostro)
            nombre = "Desconocido"
            
            # Encontrar la mejor coincidencia
            distancias_faciales = face_recognition.face_distance(rostros_conocidos, codificacion_rostro)
            mejor_coincidencia = np.argmin(distancias_faciales) if len(distancias_faciales) > 0 else -1
            
            if mejor_coincidencia >= 0 and coincidencias[mejor_coincidencia]:
                nombre = nombres_conocidos[mejor_coincidencia]
            
            nombres_rostros.append(nombre)
        
        # Mostrar resultados
        for (top, right, bottom, left), nombre in zip(ubicaciones_rostros, nombres_rostros):
            # Escalar de vuelta las ubicaciones al tamaño original
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            # Dibujar un recuadro alrededor del rostro
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            
            # Dibujar una etiqueta con el nombre
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, nombre, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)
        
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
    # 1. Primero, organiza tus imágenes en una estructura como:
    # ./personas_autorizadas/nombre_persona1/foto1.jpg, foto2.jpg, ...
    # ./personas_autorizadas/nombre_persona2/foto1.jpg, foto2.jpg, ...
    
    # 2. Crear la base de datos de rostros conocidos
    directorio_personas = "./personas_autorizadas"  # Ajusta esta ruta
    
    # Verifica si el directorio existe, si no, créalo
    if not os.path.exists(directorio_personas):
        os.makedirs(directorio_personas)
        print(f"Directorio {directorio_personas} creado. Por favor, agrega imágenes de personas.")
    
    rostros_conocidos, nombres_conocidos = crear_base_de_datos_rostros(directorio_personas)
    
    if not rostros_conocidos:
        print("No se encontraron rostros en la base de datos. Agrega imágenes al directorio.")
    else:
        # 3. Para reconocimiento en una imagen:
        # reconocimiento_imagen("ruta_a_la_imagen.jpg", rostros_conocidos, nombres_conocidos)
        
        # 4. Para reconocimiento en tiempo real con la cámara:
        reconocimiento_camara(rostros_conocidos, nombres_conocidos)