"""
用户登录接口测试
POST /api/v1/auth/login
"""
import pytest
from fastapi.testclient import TestClient


class TestLogin:
    URL = "/api/v1/auth/login"

    # ── 正常流程 ────────────────────────────────────────────────

    def test_login_success_by_username(self, client: TestClient, registered_user):
        """用用户名登录 → 200，返回 token"""
        resp = client.post(
            self.URL,
            json={
                "username": registered_user["username"],
                "password": registered_user["password"],
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "Bearer"
        assert isinstance(data["expires_in"], int)
        assert data["expires_in"] > 0

    def test_login_success_by_email(self, client: TestClient, registered_user):
        """用邮箱登录 → 200"""
        resp = client.post(
            self.URL,
            json={
                "username": registered_user["email"],
                "password": registered_user["password"],
            },
        )
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    # ── 异常流程 ────────────────────────────────────────────────

    def test_login_wrong_password(self, client: TestClient, registered_user):
        """密码错误 → 401"""
        resp = client.post(
            self.URL,
            json={
                "username": registered_user["username"],
                "password": "WrongPassword!",
            },
        )
        assert resp.status_code == 401
        assert resp.json()["code"] == "ERR_UNAUTHORIZED"

    def test_login_nonexistent_user(self, client: TestClient):
        """用户不存在 → 401"""
        resp = client.post(
            self.URL,
            json={"username": "ghost_user", "password": "P@ssw0rd123"},
        )
        assert resp.status_code == 401
        assert resp.json()["code"] == "ERR_UNAUTHORIZED"

    @pytest.mark.parametrize(
        "payload",
        [
            # 缺少 username
            {"password": "P@ssw0rd123"},
            # 缺少 password
            {"username": "testuser"},
            # 空字符串
            {"username": "", "password": ""},
        ],
    )
    def test_login_invalid_params(self, client: TestClient, payload):
        """参数不合法 → 422"""
        resp = client.post(self.URL, json=payload)
        assert resp.status_code == 422
