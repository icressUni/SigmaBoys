"""
File handling and Google Drive integration module.
"""
import os
import logging
import mimetypes
from googleapiclient.discovery import build
from ..auth.credentials import get_credentials

# Configure logging
logger = logging.getLogger(__name__)


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
