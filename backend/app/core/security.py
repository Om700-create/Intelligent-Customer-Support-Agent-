from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(subject: str, token_type: str, expires_delta: timedelta) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject), "type": token_type}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    settings = get_settings()
    minutes = expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    delta = timedelta(minutes=minutes)
    return create_token(subject, "access", delta)


def create_refresh_token(subject: str, expires_days: Optional[int] = None) -> str:
    settings = get_settings()
    days = expires_days or settings.REFRESH_TOKEN_EXPIRE_DAYS
    delta = timedelta(days=days)
    return create_token(subject, "refresh", delta)


def decode_token(token: str) -> Optional[dict[str, Any]]:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
