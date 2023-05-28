from fastapi import APIRouter, UploadFile, File, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.storage.object_storage_providers.google_object_store import (
    uploadFile,
    deleteFile,
)

upload_router = APIRouter()
app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@upload_router.post("/upload")
async def upload_file(user_name: str, file: UploadFile = File(...)):
    # Call the uploadFile function with the provided user name and uploaded file path
    uploadFile(user_name, file.file.name)
    return {"message": "File uploaded successfully"}


@upload_router.delete("/delete")
async def delete_file(user_name: str, file_name: str):
    # Call the deleteFile function with the provided user name and file name
    deleteFile(user_name, file_name)
    return {"message": "File deleted successfully"}
