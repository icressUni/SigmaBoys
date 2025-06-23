"""
Modules package for webhook server functionality.

This package contains modular components for:
- auth: Google API authentication
- forms: Google Forms integration
- files: File handling and Google Drive operations
- config: Shared configuration constants
"""

# Import main configuration
from .config import SCOPES, FORMS_DISCOVERY_DOC, FORM_ID

# Import main functions from submodules
from .auth import get_credentials
from .forms import (
    setup_watch, get_form_responses, list_all_watches, 
    delete_watch_by_id, get_existing_watches
)
from .files import (
    get_file_data, download_drive_file, download_multiple_drive_files
)

__all__ = [
    'SCOPES', 'FORMS_DISCOVERY_DOC', 'FORM_ID',
    'get_credentials',
    'setup_watch', 'get_form_responses', 'list_all_watches',
    'delete_watch_by_id', 'get_existing_watches',
    'get_file_data', 'download_drive_file', 'download_multiple_drive_files'
]
