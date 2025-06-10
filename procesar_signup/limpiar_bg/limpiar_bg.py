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

# Store the last ID retrieved from the website
last_submission_id = None

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

# Alternative route to handle submissions directly from Microsoft Power Automate
@app.route('/api/form-submission', methods=['POST'])
def receive_power_automate_submission():
    try:
        global last_submission_id
        
        # Power Automate typically sends JSON data
        data = request.json
        
        # Extract name, surname and ID
        name = data.get('nombre', '')
        surname = data.get('apellido', '')
        submission_id = data.get('id', '')
        
        # Update the last submission ID if provided
        if submission_id:
            last_submission_id = submission_id
            logger.info(f"Updated last submission ID to: {last_submission_id}")
        
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
        
        print("submission_data", submission_data)
        # Log the submission
        log_data = submission_data.copy()
        #log_data['image']['data'] = f"[Base64 string of length {len(submission_data['image']['data'])}]"
        logger.info(f"Received Power Automate submission: {json.dumps(log_data)}")
          return jsonify({'status': 'success', 'data': submission_data}), 200
        
    except Exception as e:
        logger.error(f"Error processing Power Automate submission: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Endpoint to check the last submission ID
@app.route('/api/last-submission-id', methods=['GET'])
def get_last_submission_id():
    if last_submission_id is not None:
        return jsonify({'status': 'success', 'last_id': last_submission_id})
    else:
        return jsonify({'status': 'no_data', 'message': 'No submissions received yet'}), 404

if __name__ == '__main__':
    logger.info("Starting Microsoft Forms webhook receiver")
    # Use host='0.0.0.0' to make the server publicly available
    app.run(debug=True, host='0.0.0.0', port=5000)
