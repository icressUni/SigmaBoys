# Configuring Pub/Sub with Your Webhook URL

This guide will walk you through setting up a Google Cloud Pub/Sub subscription to push notifications to your webhook.

## Prerequisites

- Your webhook server is running using `run_webhook.py`
- You have the webhook URL (automatically added to your `.env` file)
- You have access to Google Cloud Console

## Step-by-Step Guide

### 1. Start Your Webhook Server

```powershell
python run_webhook.py
```

The script will:
- Start your Flask webhook server
- Create an HTTPS tunnel using ngrok
- Display your webhook URL
- Update the `.env` file with this URL

Example output:
```
✅ ngrok is installed
✅ Webhook server started with ngrok tunnel
⏳ Waiting for ngrok to establish tunnel...
🌐 Webhook URL: https://a1b2c3d4.ngrok.io/webhook
✅ Updated .env file with webhook URL
📋 Copy this URL to use as your webhook callback URL in Google Cloud Pub/Sub
👉 Configure your Pub/Sub subscription to push to this URL
🛑 Press Ctrl+C to stop the server
```

### 2. Access Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (e.g., "labtracker-463617")

### 3. Navigate to Pub/Sub

1. In the navigation menu, find "Pub/Sub" under "Big Data"
2. Click on "Topics" in the left sidebar

### 4. Create or Select Your Topic

If your topic doesn't exist yet:
1. Click "CREATE TOPIC"
2. Enter "EnvioSolicitud" as the topic ID
3. Click "CREATE"

### 5. Create a Push Subscription

1. Select your topic from the list
2. Click "CREATE SUBSCRIPTION" at the top
3. Enter a Subscription ID (e.g., "EnvioSolicitud-webhook")
4. For Delivery Type, select "Push"
5. For Endpoint URL, paste your webhook URL from the `.env` file
   (e.g., `https://a1b2c3d4.ngrok.io/webhook`)

### 6. Configure Additional Settings (Optional)

Scroll down to see additional configuration options:

1. Acknowledgement deadline: 60 seconds (recommended)
2. Message retention duration: 7 days (default)
3. Retry policy: Set to Exponential backoff
4. Enable message ordering: If your application requires it

### 7. Create the Subscription

Click the "CREATE" button at the bottom of the page.

### 8. Test the Subscription

1. Go back to your topic
2. Click "PUBLISH MESSAGE"
3. Enter a test message in the message body
4. Click "PUBLISH"
5. Check your webhook server's logs to see if the message was received

### 9. Verify Form Watch Configuration

Make sure your Form watch is properly configured to send notifications to this Pub/Sub topic:

1. Access your webhook server's `/setup` endpoint in a browser:
   ```
   https://a1b2c3d4.ngrok.io/setup
   ```

2. This will ensure your Google Form is watching for changes and sending notifications to your Pub/Sub topic
   - If a watch already exists, you'll see a message indicating this
   - The system will use the existing watch instead of creating a duplicate

3. To view all active watches, visit:
   ```
   https://a1b2c3d4.ngrok.io/watches
   ```

4. To delete a specific watch (if needed), you can use:
   ```
   curl -X DELETE https://a1b2c3d4.ngrok.io/watches/YOUR_WATCH_ID
   ```
   Or use a tool like Postman to send a DELETE request

## Important Notes

- For development, ngrok URLs are temporary and change each time you restart ngrok
- You'll need to update your Pub/Sub subscription with the new URL each time
- The `run_webhook.py` script automatically updates the `.env` file with the latest URL
- For production, use a permanent domain with proper HTTPS certificates
