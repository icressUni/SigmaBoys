"""
Webhook server for Google Forms integration with clean architecture.
This module contains only Flask route definitions and application setup.
Business logic is separated into modules for better maintainability.
"""
import os
import json
import logging
import time
from datetime import datetime
from flask import Flask, request, jsonify

# Import from our modular structure - cleaner approach
from modules import (
    get_credentials, setup_watch, get_form_responses, 
    list_all_watches, delete_watch_by_id,
    get_file_data, download_drive_file, download_multiple_drive_files
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# File to track processed responses
PROCESSED_RESPONSES_FILE = 'processed_responses.json'

def load_processed_responses():
    """Load the list of already processed response timestamps."""
    try:
        if os.path.exists(PROCESSED_RESPONSES_FILE):
            with open(PROCESSED_RESPONSES_FILE, 'r') as f:
                return set(json.load(f))
        return set()
    except Exception as e:
        logger.error(f"Error loading processed responses: {e}")
        return set()

def save_processed_responses(processed_set):
    """Save the list of processed response timestamps."""
    try:
        with open(PROCESSED_RESPONSES_FILE, 'w') as f:
            json.dump(list(processed_set), f, indent=2)
    except Exception as e:
        logger.error(f"Error saving processed responses: {e}")

def add_processed_response(timestamp):
    """Add a response timestamp to the processed list."""
    processed = load_processed_responses()
    processed.add(timestamp)
    
    # Keep only the last 1000 processed responses to prevent file from growing too large
    if len(processed) > 1000:
        processed_list = sorted(list(processed), reverse=True)  # Sort newest first
        processed = set(processed_list[:1000])  # Keep only the 1000 most recent
        logger.info(f"Trimmed processed responses list to {len(processed)} entries")
    
    save_processed_responses(processed)
    return processed

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
                # Get ALL form responses first to identify the latest one
            all_responses = get_form_responses()
            
            if not all_responses:
                logger.info("No responses found in the form")
                return jsonify({'status': 'no_responses', 'message': 'No responses found in form'})
            
            # Load already processed responses to avoid duplicates
            processed_responses = load_processed_responses()
            
            # Sort responses by timestamp (newest first) to get the most recent response
            sorted_responses = sorted(all_responses, 
                                    key=lambda x: x.get('Timestamp', ''), 
                                    reverse=True)
            
            # Find the newest unprocessed response
            latest_unprocessed = None
            for response in sorted_responses:
                response_timestamp = response.get('Timestamp', '')
                if response_timestamp and response_timestamp not in processed_responses:
                    latest_unprocessed = response
                    break
            
            if not latest_unprocessed:
                logger.info("No new unprocessed responses found")
                return jsonify({'status': 'no_new_responses', 'message': 'No new unprocessed responses found'})
            
            # Only process the latest unprocessed response
            responses = [latest_unprocessed]
            response_timestamp = latest_unprocessed.get('Timestamp', '')
            
            logger.info(f"Processing only the latest unprocessed response with timestamp: {response_timestamp}")
            
            # Mark this response as processed
            add_processed_response(response_timestamp)
                          # Prepare the output data
            output_data = []
            for response in responses:
                # Create a unique, readable folder name for this response
                response_timestamp = response.get('Timestamp', '')
                response_name = response.get('Nombre', 'Unknown')
                
                # Create a safe folder name from timestamp and name
                if response_timestamp:
                    # Parse timestamp to create readable folder name
                    try:
                        dt = datetime.fromisoformat(response_timestamp.replace('Z', '+00:00'))
                        date_str = dt.strftime('%Y%m%d_%H%M%S')
                    except:
                        date_str = response_timestamp.replace(':', '-').replace('T', '_').split('.')[0]
                else:
                    date_str = f"response_{int(time.time())}"
                
                # Sanitize name for folder
                safe_name = "".join(c for c in response_name if c.isalnum() or c in (' ', '_', '-')).strip()
                if not safe_name:
                    safe_name = "unknown_user"
                safe_name = safe_name.replace(' ', '_')[:20]  # Limit length
                
                response_id = f"{date_str}_{safe_name}"
                
                entry = {
                    'Timestamp': response.get('Timestamp', ''),
                    'Nombre': response.get('Nombre', ''),
                    'Correo': response.get('Correo', ''),
                    'Response_ID': response_id
                }
                
                # Process photos if they exist
                if 'Foto(s) de Rostro' in response and response['Foto(s) de Rostro']:
                    photo_files = []
                    downloaded_photos = []
                    
                    logger.info(f"Processing {len(response['Foto(s) de Rostro'])} files for response {response_id}")
                    
                    for file_id in response['Foto(s) de Rostro']:
                        # Get file metadata (original method)
                        file_data = get_file_data(file_id)
                        
                        # Download the file locally with response-specific folder
                        download_result = download_drive_file(
                            file_id, 
                            download_folder="rostros_temp", 
                            message_id=response_id  # Use response ID instead of message ID
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
    watches = list_all_watches()
    return jsonify({'watches': watches})


@app.route('/watches/<watch_id>', methods=['DELETE'])
def delete_watch(watch_id):
    """Endpoint to delete a specific watch."""
    result = delete_watch_by_id(watch_id)
    if result['status'] == 'success':
        return jsonify(result)
    else:
        return jsonify(result), 500


@app.route('/processed-responses', methods=['GET'])
def get_processed_responses():
    """Endpoint to get the list of processed response timestamps."""
    processed = load_processed_responses()
    return jsonify({
        'processed_responses': sorted(list(processed), reverse=True),
        'count': len(processed)
    })


@app.route('/processed-responses', methods=['DELETE'])
def clear_processed_responses():
    """Endpoint to clear the list of processed responses (for debugging)."""
    try:
        save_processed_responses(set())
        return jsonify({'status': 'success', 'message': 'Processed responses cleared'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == '__main__':
    # For production, you should use a proper WSGI server like Gunicorn
    # and set up HTTPS with a valid certificate
    app.run(host='0.0.0.0', port=5000, debug=True)
