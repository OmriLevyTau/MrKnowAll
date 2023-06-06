import base64

from google.cloud import storage

from app.config import GC_JSON_PATH
from app.models.documents import Document, DocumentMetaData

# Load the service account key and create a storage client
client = storage.Client.from_service_account_json(GC_JSON_PATH)

def uploadFile(user_name: str, file: str, file_name: str):
    try:
        # Create a user-specific folder path within the bucket
        bucket_name = "mr-know-all"

        # Upload the file to the user's folder in the bucket
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(f"{user_name}/{file_name}")

        # blob.upload_from_string(file)
        blob.upload_from_filename(file)

    except Exception as e:
        raise e


def deleteFile(user_name: str, file_name: str):
    try:
        # Get the bucket
        bucket = client.get_bucket("mr-know-all")

        # Specify the file path within the user's folder
        file_path = f"{user_name}/{file_name}"

        # Get the blob (file) within the bucket
        blob = bucket.blob(file_path)

        # Delete the blob
        blob.delete()

    except Exception as e:
        raise e


def getFileList(user_name: str) -> list:
    try:
        bucket = storage.Bucket(client, 'mr-know-all')
        str_folder_name_on_gcs = user_name + '/'
        blobs = bucket.list_blobs(prefix=str_folder_name_on_gcs)
    except Exception as e:
        raise e

    fileList = []
    for blob in blobs:
        doc = DocumentMetaData(user_id=user_name, document_id=blob.name.rpartition('/')[-1],
                               document_size=blob.size, creation_time=blob.updated)
        fileList.append(doc)

    return fileList


def getFileContent(user_name: str, file_name: str):
    try:
        # Get the bucket
        bucket_name = "mr-know-all"
        bucket = client.get_bucket(bucket_name)

        # Specify the file path within the user's folder
        file_path = f"{user_name}/{file_name}"
        blob = bucket.blob(file_path)

        # Download the file content as bytes
        file_content = blob.download_as_bytes()

        return file_content

    except Exception as e:
        raise e


def convertDocToPdf(doc: Document, file_name: str) -> str:
    file_string = doc.pdf_encoding
    path = f'./tmp_files/{file_name}.pdf'

    with open(path, 'wb') as pdfFile:
        pdfFile.write(base64.b64decode(file_string))

    return path
