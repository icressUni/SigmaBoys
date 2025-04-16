import os
import pickle
import face_recognition

def crear_y_guardar_modelo(directorio_personas, ruta_modelo):
    """
    Crea un modelo de rostros conocidos y lo guarda en un archivo.
    """
    rostros_conocidos = []
    nombres_conocidos = []
    
    # Recorrer cada subdirectorio (persona) dentro de personas_autorizadas
    directorio_autorizadas = os.path.join(directorio_personas, "personas_autorizadas")
    if not os.path.exists(directorio_autorizadas):
        print(f"El directorio {directorio_autorizadas} no existe.")
        return
    
    for persona in os.listdir(directorio_autorizadas):
        ruta_persona = os.path.join(directorio_autorizadas, persona)
        if os.path.isdir(ruta_persona):
            # Recorrer cada imagen en el subdirectorio
            for imagen_archivo in os.listdir(ruta_persona):
                if imagen_archivo.endswith(('.jpg', '.jpeg', '.png')):
                    ruta_completa = os.path.join(ruta_persona, imagen_archivo)
                    try:
                        # Cargar la imagen y encontrar codificación facial
                        imagen = face_recognition.load_image_file(ruta_completa)
                        codificaciones = face_recognition.face_encodings(imagen)
                        
                        # Si se encontró un rostro, agregarlo al modelo
                        if codificaciones:
                            rostros_conocidos.append(codificaciones[0])
                            nombres_conocidos.append(persona)
                            print(f"Rostro de {persona} agregado al modelo")
                        else:
                            print(f"No se encontró ningún rostro en {ruta_completa}")
                    except Exception as e:
                        print(f"Error al procesar {ruta_completa}: {str(e)}")
    
    # Guardar el modelo en un archivo
    with open(ruta_modelo, 'wb') as modelo_file:
        pickle.dump({"rostros": rostros_conocidos, "nombres": nombres_conocidos}, modelo_file)
    print(f"Modelo guardado en {ruta_modelo}")

if __name__ == "__main__":
    # Directorio base que contiene la carpeta personas_autorizadas
    directorio_base = "./"
    ruta_modelo = "./modelo_rostros.pkl"
    
    # Crear y guardar el modelo
    crear_y_guardar_modelo(directorio_base, ruta_modelo)
    
    # Verificar si el modelo fue creado correctamente
    if os.path.exists(ruta_modelo):
        print(f"Modelo creado correctamente en {ruta_modelo}")
    else:
        print("Error: No se pudo crear el modelo.")
