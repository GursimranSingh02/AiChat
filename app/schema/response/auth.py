from pydantic import BaseModel


class RegisterResponseData(BaseModel):
    id: int
    name: str
    email: str


class RegisterResponse(BaseModel):
    status: int
    message: str
    data: RegisterResponseData

