import os
import json
import logging
import mimetypes
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from googleapiclient.discovery import build

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ============================================================================
# Google Forms Webhook Server with File Download Capabilities
# ============================================================================
# This server handles webhook notifications from Google Forms and can:
# 1. Receive and process form submissions via webhook
# 2. Download Google Drive files (especially images) to local storage
# 3. Filter responses by publish time to avoid reprocessing
# 4. Manage Google Forms watch notifications
# ============================================================================

# Define scopes
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/forms"
]

# Google Forms and Sheets configuration
FORMS_DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
FORM_ID = "1OVKnvfoHCatll3qkCVD9nLUEnYbyj4OcZqPVW2oLMY8" #ID for Google Form

# ============================================================================
# Authentication and API Helper Functions
# ============================================================================

def get_credentials():
    """Get and refresh Google API credentials."""
    creds = None
    # The file token.json stores the user's access and refresh tokens
    store = file.Storage("token.json")
    creds = store.get()
    
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets("client_secrets.json", SCOPES)
        creds = tools.run_flow(flow, store)
    
    return creds

def get_existing_watches(forms_service, form_id):
    """Get existing watches for a form."""
    try:
        result = forms_service.forms().watches().list(formId=form_id).execute()
        return result.get('watches', [])
    except Exception as e:
        logger.error(f"Error listing watches: {e}")
        return []

def setup_watch():
    """Setup a watch notification for the Google Form."""
    creds = get_credentials()
    
    # Build the forms service
    forms_service = discovery.build(
        "forms",
        "v1",
        http=creds.authorize(Http()),
        discoveryServiceUrl=FORMS_DISCOVERY_DOC,
        static_discovery=False,
    )
    
    # Define the watch configuration
    watch_config = {
        "watch": {
            "target": {"topic": {"topicName": "projects/labtracker-463617/topics/EnvioSolicitud"}},
            "eventType": "RESPONSES",
        }
    }
    
    # Check if watch already exists
    existing_watches = get_existing_watches(forms_service, FORM_ID)
    
    # Look for watches with the same topic and event type
    for watch in existing_watches:
        if (watch.get('target', {}).get('topic', {}).get('topicName') == 
            watch_config['watch']['target']['topic']['topicName'] and
            watch.get('eventType') == watch_config['watch']['eventType']):
            
            logger.info(f"Watch already exists: {watch}")
            return watch
    
    # Create the watch if it doesn't exist
    try:
        result = forms_service.forms().watches().create(formId=FORM_ID, body=watch_config).execute()
        logger.info(f"Watch created successfully: {result}")
        return result
    except Exception as e:
        # Handle 400 error for duplicate watch
        if "A watch for the given end user, project, form, and event type already exists" in str(e):
            logger.info("Watch already exists (from error response)")
            # Since we couldn't find it in the list but it exists, return a valid response
            return {
                "status": "exists",
                "message": "Watch already exists",
                "target": watch_config['watch']['target'],
                "eventType": watch_config['watch']['eventType']
            }
        else:
            logger.error(f"Error creating watch: {e}")
            return None

def get_form_responses(since_datetime=None):
    """Get the latest responses from the Google Form.
    
    Args:
        since_datetime (datetime, optional): If provided, only returns responses 
                                           created after this datetime.
    
    Returns:
        list: List of processed form responses
    """
    creds = get_credentials()
    
    # Build the forms service
    forms_service = discovery.build(
        "forms",
        "v1",
        http=creds.authorize(Http()),
        discoveryServiceUrl=FORMS_DISCOVERY_DOC,
        static_discovery=False,
    )
    
    # Get form response data
    try:
        form_data = forms_service.forms().get(formId=FORM_ID).execute()
        responses = forms_service.forms().responses().list(formId=FORM_ID).execute()
        
        # Get question titles and response data
        questions = {}
        
        for item in form_data.get('items', []):
            if 'questionItem' in item:
                question_id = item['questionItem']['question']['questionId']
                title = item['title']
                questions[question_id] = title
        
        # Process responses
        processed_responses = []
        for response in responses.get('responses', []):
            timestamp_str = response.get('createTime', '')
            
            # Filter by datetime if provided
            if since_datetime and timestamp_str:
                try:
                    # Parse the timestamp (Google Forms uses ISO format with 'Z')
                    # Example: "2023-06-23T10:30:45.123Z"
                    response_datetime = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                      # Convert since_datetime to UTC if it has timezone info, otherwise assume UTC
                    if since_datetime.tzinfo is None:
                        # If since_datetime is naive, assume it's UTC
                        since_datetime_utc = since_datetime.replace(tzinfo=timezone.utc)
                    else:
                        since_datetime_utc = since_datetime
                    
                    # Skip this response if it's older than the specified datetime
                    # Subtract 2 seconds from since_datetime_utc to compensate for possible delay
                    since_datetime_utc_adjusted = since_datetime_utc - timedelta(seconds=2)
                    if response_datetime <= since_datetime_utc_adjusted:
                        logger.debug(f"Skipping response with timestamp {timestamp_str} (older than {since_datetime_utc_adjusted})")
                        continue
                        
                except ValueError as e:
                    logger.warning(f"Could not parse timestamp '{timestamp_str}': {e}")
                    # Continue processing this response even if timestamp parsing fails
            
            answer_data = {}
            
            for question_id, answer in response.get('answers', {}).items():
                question_title = questions.get(question_id, question_id)
                
                # Extract the answer text based on question type
                if 'textAnswers' in answer:
                    answer_data[question_title] = answer['textAnswers']['answers'][0]['value']
                elif 'fileUploadAnswers' in answer:
                    file_ids = [file_upload['fileId'] for file_upload in answer['fileUploadAnswers']['answers']]
                    answer_data[question_title] = file_ids
              # Add timestamp
            answer_data['Timestamp'] = timestamp_str
            processed_responses.append(answer_data)
        
        logger.info(f"Retrieved {len(processed_responses)} form responses" + 
                   (f" (filtered since {since_datetime})" if since_datetime else " (no date filter)"))
        return processed_responses
    
    except Exception as e:
        logger.error(f"Error getting form responses: {e}")
        return []

def get_file_data(file_id):
    """Get file data from Google Drive."""
    creds = get_credentials()
    
    # Build the drive service
    drive_service = build('drive', 'v3', credentials=creds)
    
    try:
        # Get file metadata
        file_metadata = drive_service.files().get(fileId=file_id).execute()
          # Get file content
        file_content = drive_service.files().get_media(fileId=file_id).execute()        
        return {
            'metadata': file_metadata,
            'content': file_content
        }
    except Exception as e:
        logger.error(f"Error getting file data: {e}")
        return None

def download_drive_file(file_id, download_folder="temp_downloads", max_file_size_mb=50, message_id=None):
    """Download a Google Drive file to a local folder.
    
    Args:
        file_id (str): Google Drive file ID
        download_folder (str): Local folder to save the file (default: "temp_downloads")
        max_file_size_mb (int): Maximum file size in MB to download (default: 50MB)
        message_id (str): Optional message ID to create a subfolder (default: None)
    
    Returns:
        dict: Information about the download result
            - success (bool): Whether download was successful
            - file_path (str): Local path to downloaded file (if successful)
            - file_name (str): Name of the downloaded file
            - mime_type (str): MIME type of the file
            - is_image (bool): Whether the file is an image
            - error (str): Error message (if unsuccessful)
    """
    try:
        creds = get_credentials()
        drive_service = build('drive', 'v3', credentials=creds)
        
        # Get file metadata first
        file_metadata = drive_service.files().get(fileId=file_id).execute()
        file_name = file_metadata.get('name', f'file_{file_id}')
        mime_type = file_metadata.get('mimeType', 'application/octet-stream')
        file_size = int(file_metadata.get('size', 0))
        
        logger.info(f"Processing file: {file_name} (MIME: {mime_type}, Size: {file_size} bytes)")
        
        # Check if it's an image file
        is_image = mime_type.startswith('image/')
        
        # Check file size limit
        if file_size > max_file_size_mb * 1024 * 1024:
            error_msg = f"File size ({file_size / (1024*1024):.1f}MB) exceeds limit ({max_file_size_mb}MB)"
            logger.warning(f"Skipping {file_name}: {error_msg}")
            return {
                'success': False,
                'file_name': file_name,
                'mime_type': mime_type,
                'is_image': is_image,
                'error': error_msg
            }
        
        # Handle non-image files
        if not is_image:
            logger.info(f"Skipping non-image file: {file_name} (MIME: {mime_type})")
            return {
                'success': False,
                'file_name': file_name,
                'mime_type': mime_type,
                'is_image': is_image,
                'error': f"Non-image file type: {mime_type}"
            }
          # Create download folder structure
        final_download_folder = download_folder
        if message_id:
            # Create subfolder with message_id
            final_download_folder = os.path.join(download_folder, str(message_id))
        
        if not os.path.exists(final_download_folder):
            os.makedirs(final_download_folder)
            logger.info(f"Created download folder: {final_download_folder}")
        
        # Sanitize filename for filesystem
        safe_filename = "".join(c for c in file_name if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()
        if not safe_filename:
            safe_filename = f"image_{file_id}"
        
        # Add appropriate extension if missing
        if not os.path.splitext(safe_filename)[1]:
            extension = mimetypes.guess_extension(mime_type)
            if extension:
                safe_filename += extension
            elif is_image:
                safe_filename += '.jpg'  # Default for images
        
        file_path = os.path.join(final_download_folder, safe_filename)
        
        # Handle duplicate filenames
        counter = 1
        original_path = file_path
        while os.path.exists(file_path):
            name, ext = os.path.splitext(original_path)
            file_path = f"{name}_{counter}{ext}"
            counter += 1
        
        # Download the file content
        logger.info(f"Downloading {file_name} to {file_path}")
        file_content = drive_service.files().get_media(fileId=file_id).execute()
        
        # Write to local file
        with open(file_path, 'wb') as local_file:
            local_file.write(file_content)
        
        logger.info(f"Successfully downloaded: {file_path} ({len(file_content)} bytes)")
        
        return {
            'success': True,
            'file_path': file_path,
            'file_name': safe_filename,
            'mime_type': mime_type,
            'is_image': is_image,
            'file_size': len(file_content)
        }
        
    except Exception as e:
        error_msg = f"Error downloading file {file_id}: {str(e)}"
        logger.error(error_msg)
        return {
            'success': False,
            'file_name': f'file_{file_id}',
            'mime_type': 'unknown',
            'is_image': False,
            'error': error_msg
        }

def download_multiple_drive_files(file_ids, download_folder="temp_downloads", max_file_size_mb=50, message_id=None):
    """Download multiple Google Drive files to a local folder.
    
    Args:
        file_ids (list): List of Google Drive file IDs
        download_folder (str): Local folder to save files (default: "temp_downloads")
        max_file_size_mb (int): Maximum file size in MB per file (default: 50MB)
        message_id (str): Optional message ID to create a subfolder (default: None)
    
    Returns:
        dict: Summary of download results
            - total_files (int): Total number of files processed
            - successful_downloads (int): Number of successful downloads
            - failed_downloads (int): Number of failed downloads
            - results (list): Detailed results for each file
            - downloaded_files (list): Paths to successfully downloaded files
    """
    if not file_ids:
        logger.warning("No file IDs provided for batch download")
        return {
            'total_files': 0,
            'successful_downloads': 0,
            'failed_downloads': 0,
            'results': [],
            'downloaded_files': []
        }
    
    logger.info(f"Starting batch download of {len(file_ids)} files to {download_folder}")    
    results = []
    downloaded_files = []
    successful_downloads = 0
    failed_downloads = 0
    
    for i, file_id in enumerate(file_ids, 1):
        logger.info(f"Processing file {i}/{len(file_ids)}: {file_id}")
        
        result = download_drive_file(file_id, download_folder, max_file_size_mb, message_id)
        results.append(result)
        
        if result['success']:
            successful_downloads += 1
            downloaded_files.append(result['file_path'])
            logger.info(f"✓ Successfully downloaded: {result['file_name']}")
        else:
            failed_downloads += 1
            logger.warning(f"✗ Failed to download {file_id}: {result.get('error', 'Unknown error')}")
    
    summary = {
        'total_files': len(file_ids),
        'successful_downloads': successful_downloads,
        'failed_downloads': failed_downloads,
        'results': results,
        'downloaded_files': downloaded_files
    }
    
    logger.info(f"Batch download complete: {successful_downloads}/{len(file_ids)} files downloaded successfully")
    return summary

# ============================================================================
# Flask Routes - Webhook and API Endpoints
# ============================================================================

@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    """Handle webhook callbacks from Google Sheets/Forms."""
    if request.method == 'POST':
        try:
            # Log the received notification
            notification_data = request.get_json()
            latest_response_time = notification_data.get('message', {}).get('publishTime')
            
            # Extract message ID for folder organization
            message_id = notification_data.get('message', {}).get('messageId') or notification_data.get('messageId')
            if not message_id:
                # Fallback: use timestamp or generate unique ID
                import time
                message_id = f"msg_{int(time.time())}"
            
            logger.info(f"Message ID: {message_id}")

            logger.info(f"Received notification: {notification_data}")
            # Debug: Log the complete structure to understand the format
            logger.info(f"Full request headers: {dict(request.headers)}")
            logger.info(f"Full notification structure: {json.dumps(notification_data, indent=2)}")
          
            logger.info(f"#######Latest response time: {latest_response_time}#######")
            
            # Convert latest_response_time to datetime if available
            since_datetime = None
            if latest_response_time:
                try:
                    # Parse the publish time (typically in ISO format)
                    since_datetime = datetime.fromisoformat(latest_response_time.replace('Z', '+00:00'))
                    logger.info(f"Parsed publish time as datetime: {since_datetime}")
                except ValueError as e:
                    logger.warning(f"Could not parse publish time '{latest_response_time}': {e}")
            
            # Process the form responses (only get responses newer than publish time)
            responses = get_form_responses(since_datetime=since_datetime)
                        
            # Prepare the output data
            output_data = []
            for response in responses:
                entry = {
                    'Timestamp': response.get('Timestamp', ''),
                    'Nombre': response.get('Nombre', ''),
                    'Correo': response.get('Correo', '')
                }
                  # Process photos if they exist
                if 'Foto(s) de Rostro' in response and response['Foto(s) de Rostro']:
                    photo_files = []
                    downloaded_photos = []
                    
                    for file_id in response['Foto(s) de Rostro']:
                        # Get file metadata (original method)
                        file_data = get_file_data(file_id)
                          # Download the file locally with message_id folder
                        download_result = download_drive_file(
                            file_id, 
                            download_folder="rostros_temp", 
                            message_id=message_id
                        )
                        
                        photo_info = {
                            'file_id': file_id,
                            'name': file_data['metadata'].get('name', '') if file_data else 'unknown',
                            'mimeType': file_data['metadata'].get('mimeType', '') if file_data else 'unknown'
                        }
                        
                        # Add download information
                        if download_result['success']:
                            photo_info['downloaded'] = True
                            photo_info['local_path'] = download_result['file_path']
                            photo_info['is_image'] = download_result['is_image']
                            downloaded_photos.append(download_result['file_path'])
                            logger.info(f"Downloaded photo: {download_result['file_name']}")
                        else:
                            photo_info['downloaded'] = False
                            photo_info['download_error'] = download_result.get('error', 'Unknown error')
                            logger.warning(f"Failed to download photo {file_id}: {download_result.get('error', 'Unknown error')}")
                        
                        photo_files.append(photo_info)
                    
                    entry['Fotos_Rostro'] = photo_files
                    entry['Downloaded_Photos'] = downloaded_photos  # List of local file paths
                
                output_data.append(entry)
            print(output_data)
            return jsonify(output_data)
        
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return jsonify({'error': str(e)}), 500
    
    # For GET requests, return a simple acknowledgment
    return jsonify({'status': 'Webhook receiver is active'})

@app.route('/setup', methods=['GET'])
def setup_endpoint():
    """Endpoint to set up the watch notification."""
    result = setup_watch()
    if result:
        if result.get('status') == 'exists':
            return jsonify({
                'status': 'success', 
                'message': 'Watch already exists', 
                'result': result
            })
        return jsonify({'status': 'success', 'result': result})
    return jsonify({'status': 'error', 'message': 'Failed to set up watch'}), 500

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to get form responses."""
    responses = get_form_responses()
    return jsonify({'responses': responses})

@app.route('/download-test/<file_id>', methods=['GET'])
def download_test_endpoint(file_id):
    """Test endpoint to download a single file by ID."""
    try:
        # Get optional message_id from query parameters
        message_id = request.args.get('message_id')
        result = download_drive_file(file_id, message_id=message_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download-batch', methods=['POST'])
def download_batch_endpoint():
    """Test endpoint to download multiple files."""
    try:
        data = request.get_json()
        file_ids = data.get('file_ids', [])
        download_folder = data.get('download_folder', 'temp_downloads')
        max_file_size_mb = data.get('max_file_size_mb', 50)
        message_id = data.get('message_id')  # Add message_id support
        
        if not file_ids:
            return jsonify({'success': False, 'error': 'No file_ids provided'}), 400
        
        result = download_multiple_drive_files(file_ids, download_folder, max_file_size_mb, message_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# Watch Management Endpoints
# ============================================================================

@app.route('/watches', methods=['GET'])
def list_watches():
    """Endpoint to list all watches for the form."""
    creds = get_credentials()
    
    # Build the forms service
    forms_service = discovery.build(
        "forms",
        "v1",
        http=creds.authorize(Http()),
        discoveryServiceUrl=FORMS_DISCOVERY_DOC,
        static_discovery=False,
    )
    
    watches = get_existing_watches(forms_service, FORM_ID)
    return jsonify({'watches': watches})

@app.route('/watches/<watch_id>', methods=['DELETE'])
def delete_watch(watch_id):
    """Endpoint to delete a specific watch."""
    creds = get_credentials()
      # Build the forms service
    forms_service = discovery.build(
        "forms",
        "v1",
        http=creds.authorize(Http()),
        discoveryServiceUrl=FORMS_DISCOVERY_DOC,
        static_discovery=False,
    )
    
    try:
        forms_service.forms().watches().delete(formId=FORM_ID, watchId=watch_id).execute()
        return jsonify({'status': 'success', 'message': f'Watch {watch_id} deleted'})
    except Exception as e:
        logger.error(f"Error deleting watch: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == '__main__':
    # For production, you should use a proper WSGI server like Gunicorn
    # and set up HTTPS with a valid certificate
    app.run(host='0.0.0.0', port=5000, debug=True)
