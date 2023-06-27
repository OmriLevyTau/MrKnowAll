from pydantic import BaseModel


class ClearChatRequest(BaseModel):
    user_id: str
