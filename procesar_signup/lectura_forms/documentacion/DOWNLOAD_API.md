# Google Drive File Download API

This webhook server now includes Google Drive file download capabilities with message-based folder organization.

## Folder Structure

Files are organized by message ID:
```
rostros_temp/
├── <message_id_1>/
│   ├── image1.jpg
│   ├── image2.png
│   └── ...
├── <message_id_2>/
│   ├── photo1.jpg
│   └── ...
└── temp_downloads/
    └── <message_id_3>/
        └── files...
```

## New Endpoints

### Single File Download Test
```
GET /download-test/<file_id>?message_id=<optional_message_id>
```
Downloads a single file by Google Drive file ID, optionally organizing into a message-specific folder.

**Example:**
```bash
curl "http://localhost:5000/download-test/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms?message_id=msg_12345"
```

### Batch File Download
```
POST /download-batch
```
Downloads multiple files at once with message ID organization.

**Request Body:**
```json
{
  "file_ids": ["file_id_1", "file_id_2", "file_id_3"],
  "download_folder": "custom_folder",
  "max_file_size_mb": 50,
  "message_id": "msg_12345"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/download-batch \
  -H "Content-Type: application/json" \
  -d '{
    "file_ids": ["1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"],
    "download_folder": "rostros_temp",
    "max_file_size_mb": 25,
    "message_id": "webhook_msg_789"
  }'
```

## Features

- **Message-based Organization**: Files are organized into subfolders by message ID
- **Image Detection**: Automatically detects and handles image files  
- **Non-image Handling**: Gracefully skips non-image files with proper logging
- **File Size Limits**: Configurable maximum file size (default: 50MB)
- **Safe Filenames**: Sanitizes filenames for filesystem compatibility
- **Duplicate Handling**: Automatically handles duplicate filenames
- **Error Handling**: Comprehensive error handling and logging
- **Batch Processing**: Support for downloading multiple files at once

## Directory Structure

- `rostros_temp/<message_id>/` - Face photos from form submissions, organized by message
- `temp_downloads/<message_id>/` - General downloads, organized by message (if message_id provided)
- `temp_downloads/` - Fallback folder when no message_id is provided

## Webhook Integration

The webhook endpoint (`/webhook`) now:
1. Extracts message ID from Pub/Sub notification
2. Creates folder structure: `rostros_temp/<message_id>/`
3. Downloads all image files from form submissions into the message-specific folder
4. Provides local file paths in the response JSON

## Message ID Extraction

Message IDs are extracted from webhook notifications in this priority:
1. `notification_data.message.messageId`
2. `notification_data.messageId`  
3. Fallback: `msg_{timestamp}` if no message ID found
