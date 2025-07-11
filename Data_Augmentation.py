import cv2
import numpy as np  #Numpy 1.23.5  en la version 2.0 se borro la funcion np.sctypes
import imgaug.augmenters as iaa
import os

def augment_image(image_path, output_dir, num_augmented=10):
    # Cargar la imagen
    image = cv2.imread(image_path)
    if image is None:
        print("Error: No se pudo cargar la imagen.")
        return
    
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
    
    for i in range(num_augmented):
        augmented_image = augmenters.augment_image(image)
        output_path = os.path.join(output_dir, f"augmented_{i}.jpg")
        cv2.imwrite(output_path, augmented_image)
    
    print(f"Generadas {num_augmented} imágenes aumentadas en {output_dir}")

# Ejemplo de uso
augment_image("Hollow_Knight.jpg", "imagenes_aumentadas", num_augmented=10)
