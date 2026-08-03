from uuid import UUID

from pydantic import BaseModel


class ChatResponseData(BaseModel):
    thread_id: UUID
    thread_name: str
    query: str
    response: str


class ChatResponse(BaseModel):
    status: int
    message: str
    data: ChatResponseData
