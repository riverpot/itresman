"""
用户登出接口测试
POST /api/v1/auth/logout
"""
from fastapi.testclient import TestClient


class TestLogout:
    URL = "/api/v1/auth/logout"

    # ── 正常流程 ────────────────────────────────────────────────

    def test_logout_success(self, client: TestClient, auth_token):
        """有效 token 登出 → 200"""
        resp = client.post(
            self.URL,
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert resp.status_code == 200
        assert resp.json()["message"] == "登出成功"

    def test_token_invalid_after_logout(self, client: TestClient, auth_token):
        """登出后同一 token 再次使用 → 401（token 已失效）"""
        # 先登出
        client.post(self.URL, headers={"Authorization": f"Bearer {auth_token}"})
        # 再次尝试登出
        resp = client.post(
            self.URL,
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert resp.status_code == 401

    # ── 异常流程 ────────────────────────────────────────────────

    def test_logout_without_token(self, client: TestClient):
        """未携带 token → 401"""
        resp = client.post(self.URL)
        assert resp.status_code == 401
        assert resp.json()["code"] == "ERR_UNAUTHORIZED"

    def test_logout_invalid_token(self, client: TestClient):
        """伪造 token → 401"""
        resp = client.post(
            self.URL,
            headers={"Authorization": "Bearer invalid.token.here"},
        )
        assert resp.status_code == 401
        assert resp.json()["code"] == "ERR_UNAUTHORIZED"

    def test_logout_malformed_auth_header(self, client: TestClient):
        """Authorization 格式错误（缺少 Bearer 前缀）→ 401"""
        resp = client.post(
            self.URL,
            headers={"Authorization": "invalid-format"},
        )
        assert resp.status_code == 401
