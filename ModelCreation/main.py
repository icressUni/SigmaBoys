import os
from azure.storage.blob import BlobServiceClient
from pathlib import Path

def download_container_contents(connection_string, container_name, download_path):
    """
    Download all blobs from an Azure Storage container to a local directory.
    
    Args:
        connection_string (str): Azure Storage connection string
        container_name (str): Name of the container to download
        download_path (str): Local directory path to save files
    """
    try:
        # Create BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Get container client
        container_client = blob_service_client.get_container_client(container_name)
        
        # Create download directory if it doesn't exist
        Path(download_path).mkdir(parents=True, exist_ok=True)
        
        # List all blobs in the container
        blob_list = container_client.list_blobs()
        
        downloaded_count = 0
        
        for blob in blob_list:
            # Create local file path
            local_file_path = os.path.join(download_path, blob.name)
            
            # Create subdirectories if blob name contains path separators
            local_dir = os.path.dirname(local_file_path)
            if local_dir:
                Path(local_dir).mkdir(parents=True, exist_ok=True)
            
            # Download blob to local file
            blob_client = blob_service_client.get_blob_client(
                container=container_name, 
                blob=blob.name
            )
            
            print(f"Downloading: {blob.name}")
            
            with open(local_file_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
            
            downloaded_count += 1
        
        print(f"Successfully downloaded {downloaded_count} files to {download_path}")
        
    except Exception as e:
        print(f"Error downloading container contents: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Your Azure Storage connection string
    CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=rostros;AccountKey=P8cGoet0uIRcDvoO9SkOtUc4paCWX1KYZsR8evoS0QlODr6rwOF3qKgnNm0A5784ZoBxjckClvsq+AStCBK3wA==;EndpointSuffix=core.windows.net"
    
    # Container name to download
    CONTAINER_NAME = "public"
    
    # Local directory to save files (always in the same root as main.py)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOCAL_DOWNLOAD_PATH = os.path.join(BASE_DIR, "downloaded_files")
    
    download_container_contents(CONNECTION_STRING, CONTAINER_NAME, LOCAL_DOWNLOAD_PATH)