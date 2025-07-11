import subprocess
import time
import requests
import qrcode
import qrcode.image.svg
import io

def generate_qr(URL, as_TextArt=False):
    """Generate a QR code that points to a URL and saves it as an SVG file."""

    img = qrcode.make('URL', image_factory=qrcode.image.svg.SvgImage)

    with open('qr.svg', 'wb') as qr:
        img.save(qr)
    
    
    if as_TextArt:
        
        qr = qrcode.QRCode()
        
        qr.add_data(URL)
        f = io.StringIO()
        qr.print_ascii(out=f)
        f.seek(0)
        print("📱 QR Code generated and saved as 'qr.svg'")
        print(f.read())
    

def setup_ngrok():
    """
    Check if ngrok is installed and set up for HTTPS tunneling.
    This is a development solution - for production use a proper HTTPS server.
    """
    try:
        # Check if ngrok is installed
        subprocess.run(["ngrok", "--version"], check=True, capture_output=True)
        print("✅ ngrok is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ngrok is not installed or not in PATH")
        print("Please install ngrok from https://ngrok.com/download")
        print("After installing, run 'ngrok authtoken YOUR_AUTH_TOKEN' to authenticate")
        return False
    
    return True

def get_ngrok_url():
    """
    Get the public HTTPS URL from ngrok API.
    """
    try:
        # Query the ngrok API to get the tunnel information
        response = requests.get("http://localhost:4040/api/tunnels")
        data = response.json()
        
        # Extract the public HTTPS URL
        for tunnel in data["tunnels"]:
            if tunnel["proto"] == "https":
                return tunnel["public_url"]
        
        print("❌ No HTTPS tunnel found in ngrok")
        return None
    except Exception as e:
        print(f"❌ Error getting ngrok URL: {e}")
        return None

def run_webhook_server():
    """Run the Flask server with ngrok for HTTPS tunneling."""
    if not setup_ngrok():
        return
    
    # Start the Flask server in the background
    server_process = subprocess.Popen(["python", "app.py"])
    
    try:
        # Start ngrok to create an HTTPS tunnel to the Flask server
        ngrok_process = subprocess.Popen(
            ["ngrok", "http", "5000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print("✅ APP server started with ngrok tunnel")
        print("⏳ Waiting for ngrok to establish tunnel...")
        
        # Wait for ngrok to start and establish the tunnel
        time.sleep(3)
        
        # Get the ngrok public URL
        ngrok_url = get_ngrok_url()
        app_url = f"{ngrok_url}" if ngrok_url else None
        
        if app_url:
            print(f"🌐 APP URL: {app_url}")
            generate_qr(app_url, as_TextArt=True)
            
        else:
            print("❌ Failed to get ngrok URL. Check if ngrok is running properly.")
        
        print("🛑 Press Ctrl+C to stop the server")
        
        # Keep the script running until interrupted
        server_process.wait()
    
    except KeyboardInterrupt:
        print("\n⏹️ Stopping server...")
        server_process.terminate()
        ngrok_process.terminate()
        print("✅ Server stopped")

if __name__ == "__main__":
    run_webhook_server()
