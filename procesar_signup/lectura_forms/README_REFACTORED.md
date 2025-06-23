# Webhook Server - Modular Architecture

This is a refactored webhook server for Google Forms integration following clean architecture principles.

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your Google OAuth credentials
# See ENV_CONFIGURATION.md for detailed setup instructions
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Server

```bash
python webhook_server_refactored.py
```

## Project Structure

```
lectura_forms/
├── webhook_server_refactored.py     # Main Flask application (routes only)
├── webhook_server.py                # Original monolithic version
├── requirements.txt                 # Python dependencies
├── modules/                         # Modular business logic
│   ├── __init__.py                 # Main module exports
│   ├── config.py                   # Shared configuration constants
│   ├── auth/                       # Authentication module
│   │   ├── __init__.py
│   │   └── credentials.py          # Google API authentication
│   ├── forms/                      # Google Forms integration
│   │   ├── __init__.py
│   │   └── handlers.py             # Form operations & watch management
│   └── files/                      # File handling module
│       ├── __init__.py
│       └── handlers.py             # Google Drive file operations
├── temp_downloads/                 # Download folder for testing
└── rostros_temp/                   # Face photos organized by message ID
```

## Modular Components

### 🔐 Auth Module (`modules/auth/`)
- **`credentials.py`**: Google API authentication
  - `get_credentials()` - Handles OAuth2 authentication

### 📋 Forms Module (`modules/forms/`)
- **`handlers.py`**: Google Forms integration
  - `get_form_responses()` - Fetch form responses with date filtering
  - `setup_watch()` - Set up Pub/Sub watch notifications
  - `get_existing_watches()` - List active watches
  - `delete_watch_by_id()` - Remove specific watch
  - `list_all_watches()` - Get all watches for the form

### 📁 Files Module (`modules/files/`)
- **`handlers.py`**: Google Drive file operations
  - `get_file_data()` - Fetch file metadata and content
  - `download_drive_file()` - Download single file with message ID organization
  - `download_multiple_drive_files()` - Batch file download

### ⚙️ Configuration (`modules/config.py`)
- Shared constants and configuration
- Google API scopes, form IDs, discovery URLs

## Key Improvements

### ✅ **Clean Architecture Benefits**
1. **Separation of Concerns**: Business logic separated from web framework
2. **Modularity**: Each module handles specific functionality
3. **Testability**: Individual modules can be tested independently
4. **Maintainability**: Easier to modify specific features
5. **Reusability**: Modules can be imported and used in other projects

### ✅ **Import Structure**
```python
# Clean imports from main modules package
from modules import (
    get_credentials, setup_watch, get_form_responses,
    get_file_data, download_drive_file
)

# Or from specific modules
from modules.auth import get_credentials
from modules.forms import setup_watch, get_form_responses
from modules.files import download_drive_file
```

### ✅ **Preserved Functionality**
- All original webhook functionality maintained
- Message ID-based file organization
- Date filtering for form responses
- Watch management endpoints
- File download capabilities
- Error handling and logging

## 🔒 Security Improvements

### Environment-Based Configuration
- **No more hardcoded secrets** in `client_secrets.json`
- Google OAuth credentials stored securely in `.env` file
- Sensitive files excluded from version control via `.gitignore`
- Template file (`.env.example`) provided for easy setup

### Security Benefits
- ✅ Credentials not exposed in code repository
- ✅ Easy environment-specific configuration
- ✅ Follows security best practices
- ✅ Temporary credential files cleaned up automatically

See `ENV_CONFIGURATION.md` for detailed setup instructions.

## Usage

### Running the Server
```bash
# Using the refactored version
python webhook_server_refactored.py

# Original version still available
python webhook_server.py
```

### API Endpoints
All original endpoints remain the same:
- `POST /webhook` - Main webhook receiver
- `GET /setup` - Set up watch notifications
- `GET /test` - Test form response fetching
- `GET /download-test/<file_id>` - Test single file download
- `POST /download-batch` - Batch file download
- `GET /watches` - List all watches
- `DELETE /watches/<watch_id>` - Delete specific watch

## Benefits of Modular Design

1. **Code Organization**: Clear separation by functionality
2. **Easy Testing**: Mock individual modules for unit tests
3. **Scalability**: Add new modules without touching existing code
4. **Team Development**: Different developers can work on different modules
5. **Documentation**: Each module is self-contained with clear responsibilities

## Migration Path

1. **Phase 1**: Both versions coexist (current state)
2. **Phase 2**: Test refactored version thoroughly
3. **Phase 3**: Replace original `webhook_server.py` with refactored version
4. **Phase 4**: Remove original file once confirmed working

The refactored version maintains 100% API compatibility while providing a much cleaner, more maintainable codebase.
