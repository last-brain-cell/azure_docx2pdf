import os
import requests
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from time import perf_counter

load_dotenv()

file_type = "pdf"

access_token = os.environ.get("GRAPH_ACCESS_TOKEN")

headers = {
    'Authorization': 'Bearer ' + access_token
}


def get_file_handles(query):
    start = perf_counter()
    drive_contents = requests.get(f"{os.environ.get("GRAPH_API_ENDPOINT")}me/drive/root/search(q='{query}')",
                                  headers=headers)
    drive_contents_json = drive_contents.json()
    ids = dict()
    drive_id = drive_contents_json["value"][0]["parentReference"]["driveId"]
    for value in drive_contents_json["value"]:
        ids[value["id"]] = value["name"].strip(".docx")

    print(f"Fetching {len(drive_contents_json["value"])} files took {perf_counter() - start}sec")

    return ids, drive_id


def store_to_blob(file_data, file_name, file_path="working"):
    start = perf_counter()
    blob_service_client = BlobServiceClient.from_connection_string(
        os.getenv("BlobStorageConnString")
    )
    container_client = blob_service_client.get_container_client(os.getenv("BlobContainerName"))

    blob_client = container_client.get_blob_client(f"{file_path}/{file_name}.pdf")

    blob_client.upload_blob(
        file_data,
        blob_type="BlockBlob",
        overwrite=True,
    )
    print(f"Storing {file_name} to Blob took {perf_counter() - start}sec")

    return blob_client.url


def download_file_from_drive(file_id: str, name: str):
    start = perf_counter()
    response = requests.get(
        f"{os.environ.get("GRAPH_API_ENDPOINT")}me/drive/items/{file_id}/content?format={file_type}", headers=headers
    )

    store_to_blob(file_data=response.content, file_name=name)
    print(f"Downloading {name} from OneDrive took {perf_counter() - start}sec")


def run():
    start = perf_counter()
    file_ids, drive_id = get_file_handles("TEST for DOC Files")
    times = list()
    for file_id, file_name in file_ids.items():
        file_start = perf_counter()
        download_file_from_drive(file_id=file_id, name=file_name)
        times.append(perf_counter() - file_start)
    print(f"Entire Process took {perf_counter() - start}sec")
    print(f"Mean Time for conversion and storage is {sum(times) / len(times)}")


if __name__ == "__main__":
    run()
