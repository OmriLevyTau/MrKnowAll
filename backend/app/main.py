from fastapi import FastAPI
from app.routers.chat import chat_router
from app.routers.documents import docs_router


app = FastAPI()

app.include_router(chat_router)
app.include_router(docs_router)

@app.get("/")
async def welcome() -> dict:
    return {
        "message": "Hello from main"
    }

