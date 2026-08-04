from pydantic import BaseModel


class RegisterResponseData(BaseModel):
    id: int
    name: str
    email: str


class RegisterResponse(BaseModel):
    status: int
    message: str
    data: RegisterResponseData


class LoginResponseData(BaseModel):
    id: int
    name: str
    email: str
    access_token: str


class LoginResponse(BaseModel):
    status: int
    message: str
    data: LoginResponseData
