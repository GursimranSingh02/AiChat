from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(min_length=1, max_length=5000)
    thread_id: UUID | None = None
