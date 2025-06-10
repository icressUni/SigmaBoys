import requests
import base64
import os
import json
from PIL import Image
import io

# Test configuration
SERVER_URL = "http://localhost:5000"
IMAGE_PATH = "Felipe/captured_image_forward.jpg"  # Path to a test image

def test_post_request():
    """Test sending a POST request with an image to the server"""
    print("Testing POST request to /api/form-submission...")
    
    # Check if image exists
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: Test image not found at {IMAGE_PATH}")
        return False
    
    # Open and encode the image
    with open(IMAGE_PATH, "rb") as image_file:
        image_bytes = image_file.read()
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    
    # Prepare the payload
    payload = {
        "nombre": "Test Name",
        "apellido": "Test Surname",
        "id": "12345",  # Adding an ID to test the ID tracking
        "image": encoded_image
    }
    
    # Send the POST request
    try:
        response = requests.post(
            f"{SERVER_URL}/api/form-submission", 
            json=payload
        )
        
        # Print the response
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("POST request successful!")
            return True
        else:
            print("POST request failed.")
            return False
            
    except Exception as e:
        print(f"Error sending POST request: {str(e)}")
        return False

def test_get_request():
    """Test getting the last submission ID"""
    print("\nTesting GET request to /api/last-submission-id...")
    
    try:
        response = requests.get(f"{SERVER_URL}/api/last-submission-id")
        
        # Print the response
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("GET request successful!")
            return True
        else:
            print("GET request failed.")
            return False
            
    except Exception as e:
        print(f"Error sending GET request: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Testing Flask API ===")
    post_success = test_post_request()
    get_success = test_get_request()
    
    if post_success and get_success:
        print("\n✅ All tests passed successfully!")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
