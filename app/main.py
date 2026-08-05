from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")


def render_frontend_page(filename: str) -> str:
    content = (FRONTEND_DIR / filename).read_text(encoding="utf-8")
    return content.replace("{{BACKEND_URL}}", settings.BACKEND_URL)


@app.get("/register", include_in_schema=False)
def register_page():
    return HTMLResponse(render_frontend_page("register.html"))


@app.get("/login", include_in_schema=False)
def login_page():
    return HTMLResponse(render_frontend_page("login.html"))


@app.get("/chat", include_in_schema=False)
def chat_page():
    return HTMLResponse(render_frontend_page("chat.html"))


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    messages = []
    for error in exc.errors():
        location = ".".join(str(item) for item in error.get("loc", []) if item != "body")
        message = error.get("msg", "Invalid input")
        messages.append(f"{location}: {message}" if location else message)

    return JSONResponse(
        status_code=422,
        content={"message": "; ".join(messages) or "Invalid input"},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )


