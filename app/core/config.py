from dotenv import load_dotenv
import os
load_dotenv()

class Settings:
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = int(os.getenv("DB_PORT"))
    DB_USER: str = os.getenv("DB_USER")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")

settings = Settings()