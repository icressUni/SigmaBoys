import requests
import base64
import json

# Server URI - Assuming we're running the server locally
SERVER_URI = "http://localhost:5000/api/form-submission"

def encode_image_to_base64(image_path):
    """Convert an image file to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def test_server_connection():
    """Test sending a request to the server"""
    # Path to a test image (you can replace this with any image in your workspace)
    test_image_path = "personas_autorizadas/Felipe/captured_image_forward.jpg"
    
    try:
        # Encode the image
        base64_image = encode_image_to_base64(test_image_path)
        
        # Prepare the data payload according to your server's expectations
        payload = {
            "nombre": "Test User",
            "apellido": "Test Surname",
            "image": base64_image
        }
        
        # Make the POST request
        response = requests.post(SERVER_URI, json=payload)
        
        # Print the response
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response.json()
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    print("Testing server connection...")
    test_server_connection()
