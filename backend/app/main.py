from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.chat import chat_router
from app.routers.documents import docs_router
from app.config import EXPLORE_LOCAL_FILE
import logging
from sys import stderr

suffix = "resources\\israel-gaza.pdf"
log_output_path = EXPLORE_LOCAL_FILE[:-len(suffix)] + "log_output.log"
log_format = "%(asctime)s - %(name)s -  %(message)s"

logging.basicConfig(level=logging.DEBUG, format=log_format, filename=log_output_path)
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

