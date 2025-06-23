# Google Sheets Webhook Notification System

This system allows you to receive and process change notifications from Google Sheets/Forms via a webhook callback.

## Features

- Flask-based webhook server that listens for Google Sheets/Forms change notifications
- Automatically processes form responses when changes are detected
- Extracts key information: Timestamp, Nombre, Correo, Foto(s) de Rostro
- Handles file uploads from Google Drive
- Provides structured JSON output of form data

## Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account with API access
- Google Form and linked Google Sheet
- OAuth 2.0 client credentials (`client_secrets.json`)
- For development: ngrok (for secure webhook tunneling)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select your project
3. Enable the following APIs:
   - Google Forms API
   - Google Sheets API
   - Google Drive API
   - Cloud Pub/Sub API

4. Create OAuth 2.0 credentials:
   - Navigate to "APIs & Services" > "Credentials"
   - Create "OAuth client ID" credentials (type: Desktop application)
   - Download the credentials as `client_secrets.json` and place in the project directory

5. Set up Pub/Sub:
   - Navigate to "Pub/Sub" > "Topics"
   - Create a topic (e.g., "EnvioSolicitud")
   - Create a subscription for this topic
   - Configure the subscription to push to your webhook URL (e.g., https://your-domain.com/webhook)

### 3. First Run Authentication

The first time you run the application, it will need to authenticate:

```bash
python webhook_server.py
```

This will open a browser window for you to authenticate and create the `token.json` file.

### 4. Running the Webhook Server

For development with ngrok:

```bash
python run_webhook.py
```

The script will:
- Start the Flask server
- Start an ngrok tunnel to expose your local server
- Automatically extract the ngrok URL
- Update your `.env` file with the webhook URL
- Display the URL to use for your Pub/Sub subscription

For production:
- Deploy the Flask application using a proper WSGI server (Gunicorn, uWSGI)
- Configure with valid HTTPS certificates
- Update your Pub/Sub subscription with your production webhook URL

### 5. Setting Up the Watch Notification

Once your webhook server is running:

1. Access the `/setup` endpoint in your browser or via curl:
   ```
   https://your-domain.com/setup
   ```

2. This will create a watch notification for your Google Form

### 6. Testing the System

To test if your system is working correctly:

1. Access the `/test` endpoint:
   ```
   https://your-domain.com/test
   ```

2. This will display current form responses

3. Submit a new form response and check your webhook server logs to see the notification being processed

## API Endpoints

- `/webhook` - Receives Google Form change notifications (POST)
- `/setup` - Sets up the watch notification for the Google Form (GET)
- `/test` - Retrieves and displays current form responses (GET)
- `/watches` - Lists all active watches for the form (GET)
- `/watches/<watch_id>` - Deletes a specific watch (DELETE)

## Output Format

The webhook returns a JSON array with objects containing:

```json
[
  {
    "Timestamp": "2023-06-22T12:34:56.789Z",
    "Nombre": "John Doe",
    "Correo": "john.doe@example.com",
    "Fotos_Rostro": [
      {
        "file_id": "1ABC123def456GHI",
        "name": "face_photo.jpg",
        "mimeType": "image/jpeg"
      }
    ]
  }
]
```

## Troubleshooting

- **Authentication Issues**: Ensure `client_secrets.json` is correctly placed and has the right permissions
- **Webhook Not Receiving Notifications**: Check Pub/Sub subscription configuration and verify your webhook URL is accessible
- **File Access Issues**: Verify the OAuth scopes include Drive access

## Production Considerations

For production deployment:
- Use a proper WSGI server (Gunicorn, uWSGI)
- Configure with valid HTTPS certificates
- Implement proper error handling and recovery
- Set up monitoring and logging
- Consider rate limiting and authentication for your webhook endpoint
