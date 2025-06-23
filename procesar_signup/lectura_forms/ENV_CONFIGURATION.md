# Environment Configuration Guide

## Overview

This project now uses environment variables for sensitive configuration data instead of hardcoded JSON files. This improves security by keeping credentials out of version control.

## Setup Instructions

### 1. Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual Google OAuth credentials:

```bash
# Google OAuth2 Configuration
GOOGLE_CLIENT_ID=your_actual_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_actual_client_secret
GOOGLE_PROJECT_ID=your_actual_project_id
# ... other variables
```

### 2. Google OAuth Setup

To get your Google OAuth credentials:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Forms API, Google Drive API, and Google Sheets API
4. Go to "Credentials" > "Create Credentials" > "OAuth 2.0 Client IDs"
5. Configure the OAuth consent screen
6. Create credentials for a "Desktop application"
7. Copy the Client ID and Client Secret to your `.env` file

### 3. Security Benefits

- ✅ Credentials are not stored in version control
- ✅ Easy to use different credentials for different environments
- ✅ Reduces risk of accidentally committing secrets
- ✅ Follows security best practices

### 4. Migration from client_secrets.json

If you have an existing `client_secrets.json` file:

1. Copy the values to your `.env` file
2. Delete or move `client_secrets.json` to a secure location
3. The application will now use environment variables automatically

### 5. File Structure

```
.env                    # Your actual environment variables (not in git)
.env.example           # Template for environment variables (in git)
.gitignore             # Excludes sensitive files from git
client_secrets.json    # No longer needed (excluded from git)
```

### 6. Troubleshooting

If you get authentication errors:

1. Check that all required environment variables are set in `.env`
2. Verify your Google OAuth credentials are correct
3. Make sure the Google APIs are enabled in your project
4. Check that the redirect URI matches your OAuth configuration

### 7. Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_CLIENT_ID` | OAuth Client ID | `123456789.apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | OAuth Client Secret | `GOCSPX-...` |
| `GOOGLE_PROJECT_ID` | Google Cloud Project ID | `my-project-123` |
| `FORM_ID` | Google Form ID | `1ABC...XYZ` |
| `PUBSUB_TOPIC` | Pub/Sub topic for webhooks | `projects/my-project/topics/form-responses` |
