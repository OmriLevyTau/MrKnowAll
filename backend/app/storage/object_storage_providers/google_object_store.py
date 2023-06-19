import base64

from google.cloud import storage

from app.config import GC_JSON_PATH
from app.models.documents import Document, DocumentMetaData


class GoogleStorageClient:
    def __init__(self, credentials_path: str, bucket_name: str) -> None:
        """
        Initialize Google Storage client.
        Args:
            credentials_path (str): Path to the credentials JSON file.
            bucket_name (str): Name of the Google Storage bucket.
        """
        self.client = storage.Client.from_service_account_json(credentials_path)
        self.bucket_name = bucket_name
        self.bucket = self.client.get_bucket(self.bucket_name)

    def upload_file(self, user_name: str, file: str, file_name: str):
        """
        Uploads a file to the user's folder in the Google Storage bucket.

        Args:
            user_name (str): Name of the user.
            file (str): Path to the file to be uploaded.
            file_name (str): Name of the file in the user's folder.
        """
        try:
            # Create a user-specific folder path within the bucket
            # Upload the file to the user's folder in the bucket
            blob = self.bucket.blob(f"{user_name}/{file_name}")

            blob.upload_from_filename(file)

        except Exception as e:
            raise e

    def delete_file(self, user_name: str, file_name: str):
        try:
            # Specify the file path within the user's folder
            file_path = f"{user_name}/{file_name}"

            # Get the blob (file) within the bucket
            blob = self.bucket.blob(file_path)

            # Delete the blob
            blob.delete()

        except Exception as e:
            raise e

    def get_file_list(self, user_name: str) -> list:
        try:
            # bucket = storage.Bucket(self.client, self.bucket_name)
            str_folder_name_on_gcs = user_name + '/'
            blobs = self.bucket.list_blobs(prefix=str_folder_name_on_gcs)
        except Exception as e:
            raise e

        file_list = []
        for blob in blobs:
            doc = DocumentMetaData(user_id=user_name, document_id=blob.name.rpartition('/')[-1],
                                   document_size=blob.size, creation_time=blob.updated)
            file_list.append(doc)

        return file_list

    def get_file_content(self, user_name: str, file_name: str):
        try:
            # Specify the file path within the user's folder
            file_path = f"{user_name}/{file_name}"
            blob = self.bucket.blob(file_path)

            # Download the file content as bytes
            file_content = blob.download_as_bytes()

            return file_content

        except Exception as e:
            raise e

    @staticmethod
    def convert_doc_to_pdf(doc: Document, file_name: str) -> str:
        file_string = doc.pdf_encoding
        path = f'./tmp_files/{file_name}.pdf'

        with open(path, 'wb') as pdfFile:
            pdfFile.write(base64.b64decode(file_string))

        return path
