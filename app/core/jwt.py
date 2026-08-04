from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings


def create_access_token(*, subject: str, user_id: int, email: str) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=settings.TOKEN_VALIDITY_DAYS)
    payload = {
        "sub": subject,
        "user_id": user_id,
        "email": email,
        "iat": int(now.timestamp()),
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

