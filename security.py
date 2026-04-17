import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt

TOKEN_EXPIRES_IN = int(os.environ.get("TOKEN_EXPIRES_IN", 86400))
_SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(32))


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260000)
    return f"pbkdf2:sha256:{salt}:{dk.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        _, algo, salt, dk_hex = stored_hash.split(":")
        dk = hashlib.pbkdf2_hmac(algo, password.encode(), salt.encode(), 260000)
        return hmac.compare_digest(dk.hex(), dk_hex)
    except Exception:
        return False


def create_access_token(user_id: str, username: str) -> str:
    payload = {
        "sub": user_id,
        "username": username,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=TOKEN_EXPIRES_IN),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, _SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    """解码并验证 token，失败时抛出 jwt.PyJWTError"""
    return jwt.decode(token, _SECRET_KEY, algorithms=["HS256"])
