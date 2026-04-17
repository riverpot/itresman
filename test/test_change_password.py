"""
修改密码接口测试
PUT /api/v1/auth/password
"""
import pytest
from fastapi.testclient import TestClient


class TestChangePassword:
    URL = "/api/v1/auth/password"

    @pytest.fixture()
    def fresh_token(self, client: TestClient):
        """每个测试独立注册+登录，避免密码被上一用例改掉"""
        user = {
            "username": "pwdtestuser",
            "email": "pwdtest@example.com",
            "password": "OldP@ss123",
            "confirm_password": "OldP@ss123",
        }
        client.post("/api/v1/auth/register", json=user)
        resp = client.post(
            "/api/v1/auth/login",
            json={"username": user["username"], "password": user["password"]},
        )
        return resp.json().get("access_token", ""), user["password"]

    # ── 正常流程 ────────────────────────────────────────────────

    def test_change_password_success(self, client: TestClient, fresh_token):
        """正确旧密码 + 合法新密码 → 200"""
        token, old_pwd = fresh_token
        resp = client.put(
            self.URL,
            headers={"Authorization": f"Bearer {token}"},
            json={
                "old_password": old_pwd,
                "new_password": "NewP@ss456!",
                "confirm_new_password": "NewP@ss456!",
            },
        )
        assert resp.status_code == 200
        assert resp.json()["message"] == "密码修改成功"

    def test_new_password_works_after_change(self, client: TestClient, fresh_token):
        """改完密码后用新密码能成功登录"""
        token, old_pwd = fresh_token
        client.put(
            self.URL,
            headers={"Authorization": f"Bearer {token}"},
            json={
                "old_password": old_pwd,
                "new_password": "NewP@ss456!",
                "confirm_new_password": "NewP@ss456!",
            },
        )
        resp = client.post(
            "/api/v1/auth/login",
            json={"username": "pwdtestuser", "password": "NewP@ss456!"},
        )
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    # ── 异常流程 ────────────────────────────────────────────────

    def test_change_password_wrong_old_password(self, client: TestClient, fresh_token):
        """旧密码错误 → 400"""
        token, _ = fresh_token
        resp = client.put(
            self.URL,
            headers={"Authorization": f"Bearer {token}"},
            json={
                "old_password": "WrongOld!",
                "new_password": "NewP@ss456!",
                "confirm_new_password": "NewP@ss456!",
            },
        )
        assert resp.status_code == 400
        assert resp.json()["code"] == "ERR_WRONG_OLD_PWD"

    def test_change_password_same_as_old(self, client: TestClient, fresh_token):
        """新旧密码相同 → 422"""
        token, old_pwd = fresh_token
        resp = client.put(
            self.URL,
            headers={"Authorization": f"Bearer {token}"},
            json={
                "old_password": old_pwd,
                "new_password": old_pwd,
                "confirm_new_password": old_pwd,
            },
        )
        assert resp.status_code == 422
        assert resp.json()["code"] == "ERR_VALIDATION"

    def test_change_password_confirm_mismatch(self, client: TestClient, fresh_token):
        """两次新密码不一致 → 422"""
        token, old_pwd = fresh_token
        resp = client.put(
            self.URL,
            headers={"Authorization": f"Bearer {token}"},
            json={
                "old_password": old_pwd,
                "new_password": "NewP@ss456!",
                "confirm_new_password": "DifferentPass!",
            },
        )
        assert resp.status_code == 422
        assert resp.json()["code"] == "ERR_VALIDATION"

    def test_change_password_without_token(self, client: TestClient):
        """未携带 token → 401"""
        resp = client.put(
            self.URL,
            json={
                "old_password": "OldP@ss123",
                "new_password": "NewP@ss456!",
                "confirm_new_password": "NewP@ss456!",
            },
        )
        assert resp.status_code == 401
        assert resp.json()["code"] == "ERR_UNAUTHORIZED"

    def test_change_password_invalid_token(self, client: TestClient):
        """无效 token → 401"""
        resp = client.put(
            self.URL,
            headers={"Authorization": "Bearer fake.token.value"},
            json={
                "old_password": "OldP@ss123",
                "new_password": "NewP@ss456!",
                "confirm_new_password": "NewP@ss456!",
            },
        )
        assert resp.status_code == 401
        assert resp.json()["code"] == "ERR_UNAUTHORIZED"

    @pytest.mark.parametrize(
        "payload",
        [
            # 缺少 old_password
            {"new_password": "NewP@ss456!", "confirm_new_password": "NewP@ss456!"},
            # 新密码过短
            {
                "old_password": "OldP@ss123",
                "new_password": "abc",
                "confirm_new_password": "abc",
            },
        ],
    )
    def test_change_password_invalid_params(
        self, client: TestClient, fresh_token, payload
    ):
        """参数不合法 → 422"""
        token, _ = fresh_token
        resp = client.put(
            self.URL,
            headers={"Authorization": f"Bearer {token}"},
            json=payload,
        )
        assert resp.status_code == 422
