from dotenv import load_dotenv
import os
load_dotenv()

class Settings:
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = int(os.getenv("DB_PORT"))
    DB_USER: str = os.getenv("DB_USER")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-me")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    TOKEN_VALIDITY_DAYS: int = int(os.getenv("TOKEN_VALIDITY_DAYS", 7))

    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

    ACCESS_PAST_MESSAGES_COUNT: int = int(os.getenv("ACCESS_PAST_MESSAGES_COUNT", 5))

settings = Settings()
