import os

downloaded_files_path = os.path.join(os.path.dirname(__file__), '.', 'downloaded_files')

# Busca recursivamente todas las carpetas dentro de downloaded_files
for root, dirs, files in os.walk(downloaded_files_path):
    for dir_name in dirs:
        print(dir_name)

# Mostrar todas las imágenes dentro de la carpeta 'augmented'
augmented_path = os.path.join(os.path.dirname(__file__), '.', 'augmented')
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

for root, dirs, files in os.walk(augmented_path):
    for file in files:
        if file.lower().endswith(image_extensions):
            print(os.path.join(root, file))