import os
import tempfile

# 在导入 app 之前设置 DB_PATH，确保 database._db_path() 读到测试用路径
_db_fd, _db_path = tempfile.mkstemp(suffix=".db")
os.close(_db_fd)
os.environ["DB_PATH"] = _db_path

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="session", autouse=True)
def _cleanup_db():
    yield
    os.unlink(_db_path)


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def registered_user(client):
    """注册一个基准用户，供登录/改密测试复用"""
    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "P@ssw0rd123",
        "confirm_password": "P@ssw0rd123",
    }
    client.post("/api/v1/auth/register", json=payload)
    return payload


@pytest.fixture(scope="module")
def auth_token(client, registered_user):
    """登录并返回 access_token"""
    resp = client.post(
        "/api/v1/auth/login",
        json={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    return resp.json().get("access_token", "")
