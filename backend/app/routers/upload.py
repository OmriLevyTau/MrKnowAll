import base64
from fastapi import APIRouter, FastAPI, File, UploadFile
from app.storage.object_storage_providers.google_object_store import (
    deleteFile, uploadFile)
import os

upload_router = APIRouter()

@upload_router.post("/upload")
async def upload_file(body: dict):
    # Call the uploadFile function with the provided user name and uploaded file path
    
    # generate a UUID and write it down to a specific location!
    # print(body)
    prefix = 'data:application/pdf;base64,'
    file_string = body['file'][len(prefix):]
    # print(file_string)
    user_name = body['user_id']['email']
    file_name = body['file_name']
    
    with open(f'./tmp_files/{file_name}.pdf', 'wb') as pdfFile:
        pdfFile.write(base64.b64decode(file_string))
    
    print("user name type is:", type(user_name))
    print("user_name: ", user_name)
    uploadFile(user_name, f'.//tmp_files//{file_name}.pdf', file_name)
    os.remove(f'./tmp_files/{file_name}.pdf')
    return {"status": "ok"}


@upload_router.delete("/delete")
async def delete_file(body: dict):
    user_name = body['user_id']['email']
    file_name = body['file_name']
    print("user name is: ", user_name)
    print("file_name is: ", file_name)
    # Call the deleteFile function with the provided user name and file name
    deleteFile(user_name, file_name)
    return {"message": "File deleted successfully"}