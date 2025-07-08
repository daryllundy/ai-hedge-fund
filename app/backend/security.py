"""
Security module for API authentication and authorization.
"""
import os
import secrets
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# Security configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
API_KEY = os.getenv("API_KEY", "hedge-fund-api-key-2025")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bearer token security
security = HTTPBearer()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify JWT token or API key."""
    token = credentials.credentials
    
    # Check if it's the API key
    if token == API_KEY:
        return {"username": "api_user", "auth_type": "api_key"}
    
    # Try to decode as JWT
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username)
        return {"username": token_data.username, "auth_type": "jwt"}
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_demo_token() -> str:
    """Create a demo JWT token for testing purposes."""
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "demo_user"}, expires_delta=access_token_expires
    )
    return access_token


# Rate limiting configuration
RATE_LIMIT_CALLS = int(os.getenv("RATE_LIMIT_CALLS", "10"))
RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "60"))  # seconds