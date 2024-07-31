import os
import time

import requests
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from time import perf_counter

load_dotenv()

class AzureDocToPDF():
    def __init__(self, store_to_blob_flag: bool = False):
        self.drive_endpoint = os.environ.get("GRAPH_API_ENDPOINT")
        self.headers = {
            'Authorization': 'Bearer ' + os.environ.get("GRAPH_ACCESS_TOKEN")
        }

        self.file_type = "pdf"
        self.store_to_blob_flag = store_to_blob_flag

        self.blob_service_client = BlobServiceClient.from_connection_string(
            os.getenv("BlobStorageConnString")
        )

        self.container_client = self.blob_service_client.get_container_client(os.getenv("BlobContainerName"))

    def get_file_from_blob(self, file_path, file_name):
        blobs = self.container_client.list_blob_names()
        for blob in blobs:
            print(blob)
        blob_client = self.container_client.get_blob_client(f"test/filename.pdf")
        file = blob_client.download_blob()
        return file.readall(), file_name

    def store_to_onedrive(self, file_data, file_name):
        response = requests.put(f"{self.drive_endpoint}/me/drive/items/D4F4CD875F73E298!1447/content", headers=self.headers, data=file_data).json()
        print(response)
        return response["id"]

    def convert_and_download_file_from_drive(self, file_id: str, file_name: str):
        start = perf_counter()
        response = requests.get(
            f"{self.drive_endpoint}me/drive/items/{file_id}/content?format='{self.file_type}'",
            headers=self.headers
        )

        if self.store_to_blob_flag:
            self.store_to_blob(file_data=response.content, file_name=file_name)
        print(f"Downloading {file_name} from OneDrive took {perf_counter() - start}sec")

    def store_to_blob(self, file_data, file_name, file_path="saved"):
        start = perf_counter()
        blob_client = self.container_client.get_blob_client(f"{file_path}/{file_name}")

        blob_client.upload_blob(
            file_data,
            blob_type="BlockBlob",
            overwrite=True,
        )
        print(f"Storing {file_name} to Blob took {perf_counter() - start}sec")

        return blob_client.url

    def delete_from_drive(self, item_id):
        response = requests.delete(f"{self.drive_endpoint}me/drive/items/{item_id}", headers=self.headers)
        return response.json()

    def convert(self, file_name, file_path):
        start = perf_counter()
        file_data, file_name = self.get_file_from_blob(file_name, file_path)
        file_id = self.store_to_onedrive(file_data, file_name)
        self.convert_and_download_file_from_drive(file_id, file_name)
        self.delete_from_drive(file_id)
        time_taken = time.perf_counter() - start
        print(f"{time_taken} seconds")


if __name__ == "__main__":
    workflow = AzureDocToPDF()
    workflow.convert(file_name="filename.pdf", file_path="test")
