import os
import pickle
import json
import face_recognition

# Carga de datos de alumnos desde JSON
with open('alumnos_data.json', 'r', encoding='utf-8') as f:
    alumnos_data = json.load(f)
# Mapeo de IDs a nombres
id_to_nombre = {alumno['id']: alumno['nombre'] for alumno in alumnos_data}

def crear_y_guardar_modelo(directorio_personas, ruta_modelo):
    """
    Crea un modelo de rostros conocidos y lo guarda en un archivo.
    """
    rostros_conocidos = []
    nombres_conocidos = []

    # Recorrer cada subdirectorio (persona) dentro de downloaded_files
    directorio_autorizadas = os.path.join(directorio_personas, "downloaded_files")
    if not os.path.exists(directorio_autorizadas):
        print(f"El directorio {directorio_autorizadas} no existe.")
        return
    
    for persona in os.listdir(directorio_autorizadas):
        ruta_persona = os.path.join(directorio_autorizadas, persona)
        if os.path.isdir(ruta_persona):
            # Obtener nombre real del alumno a partir de su ID (nombre de carpeta)
            nombre = id_to_nombre.get(persona, persona)
            
            # Procesar imágenes en la carpeta principal y en la subcarpeta 'augmented'
            carpetas_a_procesar = [ruta_persona]
            ruta_augmented = os.path.join(ruta_persona, "augmented")
            if os.path.isdir(ruta_augmented):
                carpetas_a_procesar.append(ruta_augmented)
            
            for carpeta in carpetas_a_procesar:
                for imagen_archivo in os.listdir(carpeta):
                    if imagen_archivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                        ruta_completa = os.path.join(carpeta, imagen_archivo)
                        try:
                            # Cargar la imagen y encontrar codificación facial
                            imagen = face_recognition.load_image_file(ruta_completa)
                            codificaciones = face_recognition.face_encodings(imagen)
                            
                            # Si se encontró un rostro, agregarlo al modelo
                            if codificaciones:
                                rostros_conocidos.append(codificaciones[0])
                                nombres_conocidos.append(nombre)
                                print(f"Rostro de {nombre} agregado al modelo desde {ruta_completa}")
                            else:
                                print(f"No se encontró ningún rostro en {ruta_completa}")
                        except Exception as e:
                            print(f"Error al procesar {ruta_completa}: {str(e)}")
    
    # Guardar el modelo en un archivo
    with open(ruta_modelo, 'wb') as modelo_file:
        pickle.dump({"rostros": rostros_conocidos, "nombres": nombres_conocidos}, modelo_file)
    print(f"Modelo guardado en {ruta_modelo}")

if __name__ == "__main__":
    # Directorio base que contiene la carpeta downloaded_files
    directorio_base = "./"
    modelo_dir = "./model"
    ruta_modelo = os.path.join(modelo_dir, "modelo_rostros.pkl")

    # Crear la carpeta 'model' si no existe
    if not os.path.exists(modelo_dir):
        os.makedirs(modelo_dir)
    
    while True:
        entrada = input("Presiona ENTER para crear y guardar el modelo (o escribe 'back' para salir)...")
        if entrada.strip().lower() == "back":
            print("Saliendo del programa.")
            break
        
        # Crear y guardar el modelo
        crear_y_guardar_modelo(directorio_base, ruta_modelo)
        
        # Verificar si el modelo fue creado correctamente
        if os.path.exists(ruta_modelo):
            print(f"Modelo creado correctamente en {ruta_modelo}")
        else:
            print("Error: No se pudo crear el modelo.")
