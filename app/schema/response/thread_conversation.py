from uuid import UUID

from pydantic import BaseModel


class ThreadConversationItem(BaseModel):
    query: str
    response: str


class ThreadConversationResponseData(BaseModel):
    thread_id: UUID
    thread_name: str
    messages: list[ThreadConversationItem]


class ThreadConversationResponse(BaseModel):
    status: int
    message: str
    data: ThreadConversationResponseData
