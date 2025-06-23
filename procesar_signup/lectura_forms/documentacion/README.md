# Microsoft Forms Webhook Receiver

This Python service receives webhook submissions from Microsoft Forms and processes them, including extracting names, surnames, and images.

## Setup

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the application:
```
python limpiar_bg.py
```

## Endpoints

- `/webhook` - Receives form submissions with multipart form data
- `/api/form-submission` - Alternative endpoint for Power Automate that accepts JSON payloads

## Expected Form Data

- `name`: String containing the person's first name
- `surname`: String containing the person's last name
- `image`: Image file (PNG, JPG, JPEG)

## Response Format

```json
{
  "status": "success",
  "data": {
    "name": "John",
    "surname": "Doe",
    "image": {
      "format": "base64",
      "data": "base64_encoded_string",
      "shape": [height, width, channels],
      "dtype": "uint8"
    }
  }
}
```

## Deployment

For production deployment, consider:
- Using a WSGI server like Gunicorn
- Setting up HTTPS
- Implementing proper authentication
