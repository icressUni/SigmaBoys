from flask import Flask, render_template, request, jsonify
import os
import base64
import uuid
import json
from datetime import datetime

app = Flask(__name__)

# Carpetas y archivo de metadatos\ nCAPTURE_FOLDER = 'captures'
DATA_FOLDER = 'data'
CAPTURE_FOLDER = 'captures'
METADATA_FILE = os.path.join(DATA_FOLDER, 'metadata.json')

os.makedirs(CAPTURE_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

# Inicializar metadata.json si no existe
if not os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_photo', methods=['POST'])
def save_photo():
    data = request.json
    image_data = data.get('imageData')
    name = data.get('name')
    email = data.get('email')

    # Generar un ID único
    unique_id = str(uuid.uuid4())

    # Decodificar la imagen base64
    header, encoded = image_data.split(',', 1)
    ext = header.split('/')[1].split(';')[0]  # png, jpeg, etc.
    img = base64.b64decode(encoded)

    # Guardar la imagen
    image_filename = f"{unique_id}.{ext}"
    image_path = os.path.join(CAPTURE_FOLDER, image_filename)
    with open(image_path, 'wb') as f:
        f.write(img)

    # Crear entrada de metadatos
    entry = {
        'id': unique_id,
        'name': name,
        'email': email
    }

    # Cargar metadata existente
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    # Agregar y guardar de nuevo
    metadata.append(entry)
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    return jsonify({'status': 'success', 'id': unique_id})

if __name__ == '__main__':
    app.run(debug=True)