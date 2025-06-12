import base64
import cv2
import json
import logging
import numpy as np
import os
import requests
import uuid
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

from urllib.parse import urlparse, unquote
from requests.auth import HTTPBasicAuth
from requests_ntlm import HttpNtlmAuth
from typing import List, Dict, Optional, Tuple

def download_sharepoint_images(
    credentials: Dict[str, str],
    image_urls: List[str],
    temp_folder: str,
    auth_type: str = "ntlm"
) -> Dict[str, any]:
    """
    Download images from SharePoint URLs with authentication.
    
    Args:
        credentials (dict): Authentication credentials
            - For NTLM: {'username': 'domain\\username', 'password': 'password'}
            - For Basic: {'username': 'username', 'password': 'password'}
            - For Bearer: {'token': 'bearer_token'}
        image_urls (list): List of SharePoint image URLs
        temp_folder (str): Path to existing temporary folder
        auth_type (str): Authentication type ('ntlm', 'basic', 'bearer')
    
    Returns:
        dict: Results summary with success/failure counts and details
    """
    
    # Validate inputs
    if not os.path.exists(temp_folder):
        raise ValueError(f"Temporary folder does not exist: {temp_folder}")
    
    if not image_urls:
        raise ValueError("No image URLs provided")
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Results tracking
    results = {
        'total_urls': len(image_urls),
        'successful_downloads': 0,
        'failed_downloads': 0,
        'success_details': [],
        'error_details': [],
        'downloaded_files': []
    }
    
    # Setup authentication
    auth = _setup_authentication(credentials, auth_type)
    if auth is None:
        results['error_details'].append("Failed to setup authentication")
        return results
    
    # Setup session with common headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'image/*,*/*;q=0.8'
    })
    
    if auth_type != 'bearer':
        session.auth = auth
    else:
        session.headers['Authorization'] = f"Bearer {credentials.get('token')}"
    
    # Process each URL
    for i, url in enumerate(image_urls, 1):
        logger.info(f"Processing image {i}/{len(image_urls)}: {url}")
        
        try:
            # Download image
            success, file_path, error_msg = _download_single_image(
                session, url, temp_folder, logger
            )
            
            if success:
                results['successful_downloads'] += 1
                results['success_details'].append({
                    'url': url,
                    'file_path': file_path,
                    'index': i
                })
                results['downloaded_files'].append(file_path)
                logger.info(f"Successfully downloaded: {file_path}")
            else:
                results['failed_downloads'] += 1
                results['error_details'].append({
                    'url': url,
                    'error': error_msg,
                    'index': i
                })
                logger.error(f"Failed to download {url}: {error_msg}")
                
        except Exception as e:
            results['failed_downloads'] += 1
            error_msg = f"Unexpected error: {str(e)}"
            results['error_details'].append({
                'url': url,
                'error': error_msg,
                'index': i
            })
            logger.error(f"Unexpected error for {url}: {error_msg}")
    
    # Final summary
    logger.info(f"Download complete: {results['successful_downloads']}/{results['total_urls']} successful")
    
    return results


def _setup_authentication(credentials: Dict[str, str], auth_type: str):
    """Setup authentication based on type."""
    try:
        if auth_type.lower() == 'ntlm':
            username = credentials.get('username')
            password = credentials.get('password')
            if not username or not password:
                raise ValueError("NTLM authentication requires username and password")
            return HttpNtlmAuth(username, password)
        
        elif auth_type.lower() == 'basic':
            username = credentials.get('username')
            password = credentials.get('password')
            if not username or not password:
                raise ValueError("Basic authentication requires username and password")
            return HTTPBasicAuth(username, password)
        
        elif auth_type.lower() == 'bearer':
            token = credentials.get('token')
            if not token:
                raise ValueError("Bearer authentication requires token")
            return None  # Handled in headers
        
        else:
            raise ValueError(f"Unsupported authentication type: {auth_type}")
            
    except Exception as e:
        logging.error(f"Authentication setup failed: {str(e)}")
        return None


def _download_single_image(
    session: requests.Session, 
    url: str, 
    temp_folder: str, 
    logger: logging.Logger
) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Download a single image from SharePoint.
    
    Returns:
        tuple: (success: bool, file_path: str|None, error_message: str|None)
    """
    try:
        # Validate URL
        if not url or not url.strip():
            return False, None, "Empty or invalid URL"
        
        # Parse URL to get filename
        parsed_url = urlparse(url)
        filename = os.path.basename(unquote(parsed_url.path))
        
        # Generate filename if not available from URL
        if not filename or '.' not in filename:
            filename = f"image_{hash(url) % 10000}.jpg"
        
        # Ensure filename is safe
        filename = _sanitize_filename(filename)
        file_path = os.path.join(temp_folder, filename)
        
        # Handle duplicate filenames
        counter = 1
        base_name, ext = os.path.splitext(filename)
        while os.path.exists(file_path):
            new_filename = f"{base_name}_{counter}{ext}"
            file_path = os.path.join(temp_folder, new_filename)
            counter += 1
        
        # Download with timeout and streaming
        response = session.get(url, timeout=30, stream=True, allow_redirects=True)
        response.raise_for_status()
        
        # Verify content type - With SharePoint we need to be more flexible
        content_type = response.headers.get('content-type', '').lower()
        
        # If we got HTML but the URL appears to be an image, try to proceed anyway
        if 'text/html' in content_type and any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']):
            logger.warning(f"SharePoint returned HTML for an image URL. Attempting to save anyway: {url}")
            # Examine the first few bytes to check if it looks like an image
            first_bytes = next(response.iter_content(256))
            
            # Check for common image file signatures
            is_likely_image = False
            if first_bytes.startswith(b'\xff\xd8'):  # JPEG
                is_likely_image = True
                if not filename.lower().endswith(('.jpg', '.jpeg')):
                    filename = f"{os.path.splitext(filename)[0]}.jpg"
                    file_path = os.path.join(temp_folder, filename)
            elif first_bytes.startswith(b'\x89PNG\r\n\x1a\n'):  # PNG
                is_likely_image = True
                if not filename.lower().endswith('.png'):
                    filename = f"{os.path.splitext(filename)[0]}.png"
                    file_path = os.path.join(temp_folder, filename)
            elif first_bytes.startswith(b'GIF8'):  # GIF
                is_likely_image = True
                if not filename.lower().endswith('.gif'):
                    filename = f"{os.path.splitext(filename)[0]}.gif"
                    file_path = os.path.join(temp_folder, filename)
            
            if not is_likely_image:
                # If it doesn't look like an image, save the HTML for debugging
                debug_file = os.path.join(temp_folder, f"debug_{hash(url) % 10000}.html")
                with open(debug_file, 'wb') as f:
                    f.write(first_bytes)
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return False, None, f"SharePoint returned HTML instead of an image. Debug content saved to {debug_file}"
            
            # Reset response since we consumed some content
            response = session.get(url, timeout=30, stream=True, allow_redirects=True)
            response.raise_for_status()
        
        # For non-HTML content, do a more standard verification
        elif not any(img_type in content_type for img_type in ['image/', 'application/octet-stream', 'binary/', 'application/octet']):
            return False, None, f"Invalid content type: {content_type}"
        
        # Save file
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        # Verify file was created and has content
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return False, None, "Downloaded file is empty or not created"
        
        return True, file_path, None
        
    except requests.exceptions.Timeout:
        return False, None, "Request timeout"
    except requests.exceptions.ConnectionError:
        return False, None, "Connection error"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return False, None, "Authentication failed (401 Unauthorized)"
        elif e.response.status_code == 403:
            return False, None, "Access forbidden (403 Forbidden)"
        elif e.response.status_code == 404:
            return False, None, "Image not found (404 Not Found)"
        else:
            return False, None, f"HTTP error {e.response.status_code}: {str(e)}"
    except requests.exceptions.RequestException as e:
        return False, None, f"Request error: {str(e)}"
    except IOError as e:
        return False, None, f"File I/O error: {str(e)}"
    except Exception as e:
        return False, None, f"Unexpected error: {str(e)}"


def _sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system usage."""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit length and ensure extension
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:250] + ext
    
    return filename

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

def link_to_image(link):
    pass

def clean_image_url(image_array):
    """
    Process the image data from the JSON payload.
    Extracts all URLs from the 'link' attributes in the image array.
    Returns a list of valid image file paths (downloaded from URLs).
    """
    image_paths = []
    
    for img_obj in image_array:
        print(f"Processing image object: {img_obj}")
        if isinstance(img_obj, str):
            # Sometimes the array items might be JSON strings
            try:
                img_obj = json.loads(img_obj)
            except json.JSONDecodeError:
                logger.warning(f"Could not parse image object as JSON: {img_obj[:100]}...")
                continue
        
        # Extract the link URL
        if isinstance(img_obj, dict) and 'link' in img_obj:
            image_url = img_obj['link']
            logger.info(f"Found image URL: {image_url}")
            print(f"image_url: {image_url}")
            image_paths.append(image_url)
            
            
    return image_paths

# Alternative route to handle submissions directly from Microsoft Power Automate
@app.route('/api/form-submission', methods=['POST'])
def receive_power_automate_submission():
    try:
        # Power Automate typically sends JSON data
        data = request.json
        print(f"Received data: {data}")
        
        # Log the key parameters we received
        name = data.get('name', '')
        surname = data.get('surname', '')
        submission_id = data.get('id', '')
        images = json.loads(data.get('images', '[]'))
        link_array = clean_image_url(images)
         
        print(f"name: {name}, surname: {surname}, submission_id: {submission_id}, images: {images}")
        
        global last_submission_id
        if submission_id:
            last_submission_id = submission_id
            logger.info(f"Updated last submission ID to: {last_submission_id}")

        print("link_array: ", link_array)

        credentials = {
        'username': 'alumnosuaicl\\icressall@alumnos.uai.cl',
        'password': 'o5Tvi@m'
        }
        results = download_sharepoint_images(
        credentials=credentials,
        image_urls=link_array,
        temp_folder=UPLOAD_FOLDER,
        auth_type='ntlm'
    )
     
        # For now, just return a success response with the received data
        return jsonify({'status': 'success', 'data': data}), 200

        download_sharepoint_images
        
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
