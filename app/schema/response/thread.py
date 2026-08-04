from uuid import UUID

from pydantic import BaseModel


class ThreadListItem(BaseModel):
    thread_id: UUID
    thread_name: str


class ThreadListResponseData(BaseModel):
    threads: list[ThreadListItem]
    page: int
    limit: int
    total: int
    total_pages: int


class ThreadListResponse(BaseModel):
    status: int
    message: str
    data: ThreadListResponseData
