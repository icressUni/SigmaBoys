"""
Configuration constants for the webhook server.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define scopes for Google APIs
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/forms"
]

# Google Forms and Sheets configuration
FORMS_DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
FORM_ID = os.getenv("FORM_ID", "1OVKnvfoHCatll3qkCVD9nLUEnYbyj4OcZqPVW2oLMY8")

# Google OAuth2 credentials from environment
GOOGLE_CLIENT_SECRETS = {
    "installed": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
        "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_CERT_URL"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")]
    }
}
