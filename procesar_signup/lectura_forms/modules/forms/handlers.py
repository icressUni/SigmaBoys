"""
Google Forms integration module.
"""
import logging
from datetime import datetime, timezone, timedelta
from apiclient import discovery
from httplib2 import Http
from ..auth.credentials import get_credentials
from ..config import FORMS_DISCOVERY_DOC, FORM_ID

# Configure logging
logger = logging.getLogger(__name__)


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


def delete_watch_by_id(watch_id):
    """Delete a specific watch by ID."""
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
        return {'status': 'success', 'message': f'Watch {watch_id} deleted'}
    except Exception as e:
        logger.error(f"Error deleting watch: {e}")
        return {'status': 'error', 'message': str(e)}


def list_all_watches():
    """List all watches for the form."""
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
    return watches
