from app.routers.chat import chat_router
from app.routers.documents import docs_router

import uvicorn
import firebase_admin
import json

from firebase_admin import credentials, auth
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.config import SERVICE_ACCOUNT_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# create Firebase connection.
cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
firebase = firebase_admin.initialize_app(cred)


app = FastAPI()

app.include_router(chat_router)
app.include_router(docs_router)


app.add_middleware(

    # allow cross-origin requests from your frontend application to your FastAPI backend.
    CORSMiddleware,
    # Update with your frontend URL
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization"],
    expose_headers=["Authorization"],  # Expose all headers
)


@app.get("/")
async def welcome() -> dict:
    return {
        "message": "Hello from main"
    }

# Custom route for handling OPTIONS requests


@app.middleware("http")
async def middleware_validatation(request: Request, call_next):
    # Get the authorization header
    # get the token data, passed in headers

    if (request.method == "OPTIONS"):
        response = await call_next(request)
        return response

    jwt = request.headers.get('authorization')
    # token = request.query_params.get("access_token")
    if jwt:
        try:
            # Extract the token from the authorization header
            _, token = jwt.split(" ")
            # Verify and decode the Firebase token. If it can’t verify the token, there will be an error thrown. If it can, we proceed as we should have.
            decoded_token = auth.verify_id_token(token)
            # Store the decoded token in request state for later use
            request.state.user = decoded_token

            response = await call_next(request)
            return response

        except ValueError as e:
            print("error in authorization from middleware")
            raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
