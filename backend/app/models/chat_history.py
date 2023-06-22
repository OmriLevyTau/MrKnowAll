from pydantic import BaseModel


class Clear_chat_request(BaseModel):
    user_id: str
