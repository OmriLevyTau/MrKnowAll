from google.cloud import storage
import base64

# Load the service account key and create a storage client
client = storage.Client.from_service_account_json(
    r"C:\Users\Talya\Documents\Studies\TAUComputerScience\2023B\GoogleWorkshop\MrKnowAll\backend\app\storage\object_storage_providers\mr-know-all-387618-f2bc1e5e3b0b.json"
)


def uploadFile(user_name: str, file: str, file_name: str):
    # Create a user-specific folder path within the bucket
    bucket_name = "mr-know-all"

    # Upload the file to the user's folder in the bucket
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(f"{user_name}/{file_name}")

    # blob.upload_from_string(file)
    blob.upload_from_filename(file)


def deleteFile(user_name: str, file_name: str):
    # Instantiate the client
    client = storage.Client()

    # Get the bucket
    bucket = client.get_bucket("mr-know-all")

    # Specify the file path within the user's folder
    file_path = f"{user_name}/{file_name}"

    # Get the blob (file) within the bucket
    blob = bucket.blob(file_path)

    # Delete the blob
    blob.delete()


def getFileList(user_name: str) -> list:
    bucket = storage.Bucket(client, 'mr-know-all')
    str_folder_name_on_gcs = user_name + '/'
    blobs = bucket.list_blobs(prefix=str_folder_name_on_gcs)
    fileList = []
    for blob in blobs:
        fileList.append(blob.name.rpartition('/')[-1])

    return fileList


def getFileContent(user_name: str, file_name: str):
    # Get the bucket
    bucket_name = "mr-know-all"
    bucket = client.get_bucket(bucket_name)

    # Specify the file path within the user's folder
    file_path = f"{user_name}/{file_name}"
    blob = bucket.blob(file_path)

    # Download the file content as bytes
    file_content = blob.download_as_bytes()

    return file_content
