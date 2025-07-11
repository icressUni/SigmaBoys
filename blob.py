from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

storage_account_name = "rostros"
storage_account_key = "uAQmF0ywSUJrO82FnmikIBkxZp8HOW+Uk9nN4tvYN7iEebOU22TwGvqeXBmetS9K6Aykr01gtWu/+ASt4Ww6og=="
connection_string = "DefaultEndpointsProtocol=https;AccountName=rostros;AccountKey=P8cGoet0uIRcDvoO9SkOtUc4paCWX1KYZsR8evoS0QlODr6rwOF3qKgnNm0A5784ZoBxjckClvsq+AStCBK3wA==;EndpointSuffix=core.windows.net"
container_name = "public"

def upload_blob(file_path, blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)
    print(f"Blob '{blob_name}' uploaded successfully to container '{container_name}'.")

upload_blob("MAMBO.png", "MAMBO.png")   