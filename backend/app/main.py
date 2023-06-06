from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.chat import chat_router
from app.routers.documents import docs_router

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
