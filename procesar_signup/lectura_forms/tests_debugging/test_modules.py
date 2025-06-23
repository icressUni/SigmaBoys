#!/usr/bin/env python3
"""
Test script to verify modular imports work correctly.
Run this to ensure the refactored structure is functional.
"""

def test_imports():
    """Test that all modules can be imported successfully."""
    try:
        print("Testing modular imports...")
          # Test config import
        from modules.config import SCOPES, FORMS_DISCOVERY_DOC, FORM_ID, GOOGLE_CLIENT_SECRETS
        print("✓ Config module imported successfully")
        
        # Test environment configuration loading
        if GOOGLE_CLIENT_SECRETS and 'installed' in GOOGLE_CLIENT_SECRETS:
            client_id = GOOGLE_CLIENT_SECRETS['installed'].get('client_id')
            if client_id and client_id != 'your_client_id_here.apps.googleusercontent.com':
                print("✓ Environment configuration loaded from .env")
            else:
                print("⚠ Warning: Using example configuration - update .env file")
        else:
            print("⚠ Warning: GOOGLE_CLIENT_SECRETS not properly configured")
        
        # Test auth module
        from modules.auth import get_credentials
        print("✓ Auth module imported successfully")
        
        # Test forms module
        from modules.forms import (
            setup_watch, get_form_responses, list_all_watches,
            delete_watch_by_id, get_existing_watches
        )
        print("✓ Forms module imported successfully")
        
        # Test files module
        from modules.files import (
            get_file_data, download_drive_file, download_multiple_drive_files
        )
        print("✓ Files module imported successfully")
        
        # Test main modules package import
        from modules import (
            get_credentials as creds_main,
            setup_watch as setup_main,
            get_form_responses as responses_main,
            download_drive_file as download_main
        )
        print("✓ Main modules package imported successfully")
        
        print("\n🎉 All imports successful! Modular structure is working correctly.")
        print(f"📊 Found {len(SCOPES)} API scopes configured")
        print(f"📋 Form ID: {FORM_ID}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = test_imports()
    exit(0 if success else 1)
