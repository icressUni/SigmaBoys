"""
Authentication module for Google APIs.
"""
import logging
import json
import tempfile
import os
from oauth2client import client, file, tools
from ..config import SCOPES, GOOGLE_CLIENT_SECRETS

# Configure logging
logger = logging.getLogger(__name__)


def get_credentials():
    """Get and refresh Google API credentials."""
    creds = None
    # The file token.json stores the user's access and refresh tokens
    store = file.Storage("token.json")
    creds = store.get()
    
    if not creds or creds.invalid:
        # Create a temporary client secrets file from environment variables
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(GOOGLE_CLIENT_SECRETS, temp_file)
            temp_secrets_path = temp_file.name
        
        try:
            flow = client.flow_from_clientsecrets(temp_secrets_path, SCOPES)
            creds = tools.run_flow(flow, store)
        finally:
            # Clean up temporary file
            os.unlink(temp_secrets_path)
    
    return creds
