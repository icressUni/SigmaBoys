import base64
import cv2
import json
import logging
import numpy as np
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure upload folder for temporary storage
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_to_base64(image_array):
    """Convert a numpy image array to base64 string"""
    success, encoded_image = cv2.imencode('.png', image_array)
    if success:
        return base64.b64encode(encoded_image).decode('utf-8')
    return None

@app.route('/webhook', methods=['POST'])
def receive_form_submission():
    try:
        # Extract form data
        form_data = request.form
        
        # Get name and surname
        name = form_data.get('name', '')
        surname = form_data.get('surname', '')
        
        # Check if the post request has the file part
        if 'image' not in request.files:
            return jsonify({'error': 'No image found in submission'}), 400
            
        file = request.files['image']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        if file and allowed_file(file.filename):
            # Secure the filename and save temporarily
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Read the image with OpenCV
            image = cv2.imread(filepath)
            
            # Process the image if needed (e.g., resize, convert color)
            # image = cv2.resize(image, (width, height))
            
            # Create JSON with form data and image
            submission_data = {
                'name': name,
                'surname': surname,
                'image': {
                    'format': 'base64',
                    'data': image_to_base64(image),
                    'shape': image.shape,
                    'dtype': str(image.dtype)
                }
            }
            
            # Log the submission (excluding the image data for brevity)
            log_data = submission_data.copy()
            log_data['image']['data'] = f"[Base64 string of length {len(submission_data['image']['data'])}]"
            logger.info(f"Received form submission: {json.dumps(log_data)}")
            
            # Clean up the temporary file
            os.remove(filepath)
            
            return jsonify({'status': 'success', 'data': submission_data}), 200
        
        return jsonify({'error': 'File type not allowed'}), 400
        
    except Exception as e:
        logger.error(f"Error processing form submission: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Alternative route to handle submissions directly from Microsoft Power Automate
@app.route('/api/form-submission', methods=['POST'])
def receive_power_automate_submission():
    try:
        # Power Automate typically sends JSON data
        data = request.json
        
        # Extract name and surname
        name = data.get('name', '')
        surname = data.get('surname', '')
        
        # Extract image data (assuming it's already base64 encoded)
        image_data = data.get('image', '')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Create submission data
        submission_data = {
            'name': name,
            'surname': surname,
            'image': {
                'format': 'base64',
                'data': image_to_base64(image),
                'shape': image.shape,
                'dtype': str(image.dtype)
            }
        }
        
        # Log the submission
        log_data = submission_data.copy()
        log_data['image']['data'] = f"[Base64 string of length {len(submission_data['image']['data'])}]"
        logger.info(f"Received Power Automate submission: {json.dumps(log_data)}")
        
        return jsonify({'status': 'success', 'data': submission_data}), 200
        
    except Exception as e:
        logger.error(f"Error processing Power Automate submission: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Microsoft Forms webhook receiver")
    # Use host='0.0.0.0' to make the server publicly available
    app.run(debug=True, host='0.0.0.0', port=5000)
