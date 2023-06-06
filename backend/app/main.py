from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.routers.chat import chat_router
from app.routers.documents import docs_router
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


@app.get("/")
async def welcome() -> dict:
    return {
        "message": "Hello from main"
    }
