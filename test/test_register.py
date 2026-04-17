"""
用户注册接口测试
POST /api/v1/auth/register
"""
import pytest
from fastapi.testclient import TestClient


class TestRegister:
    URL = "/api/v1/auth/register"

    # ── 正常流程 ────────────────────────────────────────────────

    def test_register_success(self, client: TestClient):
        resp = client.post(
            self.URL,
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "P@ssw0rd123",
                "confirm_password": "P@ssw0rd123",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert "user_id" in data
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "created_at" in data

    # ── 异常流程 ────────────────────────────────────────────────

    def test_register_duplicate_username(self, client: TestClient, registered_user):
        """用户名已存在 → 409"""
        resp = client.post(
            self.URL,
            json={
                "username": registered_user["username"],
                "email": "another@example.com",
                "password": "P@ssw0rd123",
                "confirm_password": "P@ssw0rd123",
            },
        )
        assert resp.status_code == 409
        assert resp.json()["code"] == "ERR_CONFLICT"

    def test_register_duplicate_email(self, client: TestClient, registered_user):
        """邮箱已注册 → 409"""
        resp = client.post(
            self.URL,
            json={
                "username": "anotheruser",
                "email": registered_user["email"],
                "password": "P@ssw0rd123",
                "confirm_password": "P@ssw0rd123",
            },
        )
        assert resp.status_code == 409
        assert resp.json()["code"] == "ERR_CONFLICT"

    def test_register_password_mismatch(self, client: TestClient):
        """两次密码不一致 → 422"""
        resp = client.post(
            self.URL,
            json={
                "username": "mismatchuser",
                "email": "mismatch@example.com",
                "password": "P@ssw0rd123",
                "confirm_password": "WrongPass!",
            },
        )
        assert resp.status_code == 422
        assert resp.json()["code"] == "ERR_VALIDATION"

    @pytest.mark.parametrize(
        "payload",
        [
            # 缺少 username
            {"email": "x@x.com", "password": "P@ss1234", "confirm_password": "P@ss1234"},
            # 缺少 email
            {"username": "u", "password": "P@ss1234", "confirm_password": "P@ss1234"},
            # 密码过短
            {
                "username": "shortpwd",
                "email": "s@s.com",
                "password": "abc",
                "confirm_password": "abc",
            },
        ],
    )
    def test_register_invalid_params(self, client: TestClient, payload):
        """参数不合法 → 422"""
        resp = client.post(self.URL, json=payload)
        assert resp.status_code == 422
