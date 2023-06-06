from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from app.routers.chat import chat_router
from app.routers.documents import docs_router
from app.routers.upload import upload_router

from google.cloud import storage

from app.storage.object_storage_providers.google_object_store import (
    getFileList, getFileContent)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(docs_router)
app.include_router(upload_router)


@app.get("/")
async def welcome() -> dict:
    return {
        "message": "Hello from main"
    }


@app.get("/files/{user_name}")
async def filesByUser(user_name: str) -> list:
    return getFileList(user_name)


@app.get("/files/{user_name}/{file_name}")
async def get_file(user_name: str, file_name: str, response: Response):
    # Retrieve the file content from GCS
    file_content = getFileContent(user_name, file_name)

    if file_content is None:
        return Response(status_code=404)

    content_type = "application/pdf"  # Adjust as needed

    # Stream the file content as the response body
    return StreamingResponse(
        iter([file_content]),
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename={file_name}.pdf"},)
