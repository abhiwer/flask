
import os
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient

from appconstant import CONNECTION_STRING
from appconstant import BLOB_CONTAINER

MY_CONNECTION_STRING = CONNECTION_STRING
MY_BLOB_CONTAINER = BLOB_CONTAINER


LOCAL_BLOB_PATH = "static/download"


class AzureBlobFileDownloader:
    def __init__(self):
        print("Intializing Azure Blob File Downloader")

        self.blob_service_client = BlobServiceClient.from_connection_string(
            MY_CONNECTION_STRING)
        self.my_container = self.blob_service_client.get_container_client(
            MY_BLOB_CONTAINER)

    def save_blob(self, file_name, file_content):
        download_file_path = os.path.join(LOCAL_BLOB_PATH, file_name)

        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)

        with open(download_file_path, "wb") as file:
            file.write(file_content)

    def download_all_blobs_in_container(self):
        my_blobs = self.my_container.list_blobs()
        for blob in my_blobs:
            print("Downloading file - " + blob.name)
            bytes = self.my_container.get_blob_client(
                blob).download_blob().readall()
            self.save_blob(blob.name, bytes)
