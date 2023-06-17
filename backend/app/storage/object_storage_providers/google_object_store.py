import base64
from google.cloud import storage
from app.config import GC_JSON_PATH
from app.models.documents import Document, DocumentMetaData


class GoogleCloudStorage:
    def __init__(self):
        self.client = storage.Client.from_service_account_json(GC_JSON_PATH)
        self.bucket_name = "mr-know-all"

    def uploadFile(self, user_name: str, file: str, file_name: str):
        try:
            bucket = self.client.get_bucket(self.bucket_name)
            blob = bucket.blob(f"{user_name}/{file_name}")
            blob.upload_from_filename(file)
        except Exception as e:
            raise e

    def deleteFile(self, user_name: str, file_name: str):
        try:
            bucket = self.client.get_bucket(self.bucket_name)
            file_path = f"{user_name}/{file_name}"
            blob = bucket.blob(file_path)
            blob.delete()
        except Exception as e:
            raise e

    def getFileList(self, user_name: str) -> list:
        try:
            bucket = self.client.get_bucket(self.bucket_name)
            str_folder_name_on_gcs = user_name + '/'
            blobs = bucket.list_blobs(prefix=str_folder_name_on_gcs)
        except Exception as e:
            raise e

        fileList = []
        for blob in blobs:
            doc = DocumentMetaData(
                user_id=user_name,
                document_id=blob.name.rpartition('/')[-1],
                document_size=blob.size,
                creation_time=blob.updated
            )
            fileList.append(doc)

        return fileList

    def getFileContent(self, user_name: str, file_name: str):
        try:
            bucket = self.client.get_bucket(self.bucket_name)
            file_path = f"{user_name}/{file_name}"
            blob = bucket.blob(file_path)
            file_content = blob.download_as_bytes()
            return file_content
        except Exception as e:
            raise e

    def convertDocToPdf(self, doc: Document, file_name: str) -> str:
        file_string = doc.pdf_encoding
        path = f'./tmp_files/{file_name}.pdf'

        with open(path, 'wb') as pdfFile:
            pdfFile.write(base64.b64decode(file_string))

        return path
