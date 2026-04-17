import uuid
from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from database import get_db
from schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse, ErrorResponse
from security import hash_password, verify_password, create_access_token, TOKEN_EXPIRES_IN

router = APIRouter(prefix="/api/v1/auth", tags=["用户管理"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=201,
    responses={409: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
)
def register(body: RegisterRequest):
    with get_db() as conn:
        # 检查用户名重复
        if conn.execute("SELECT 1 FROM users WHERE username = ?", (body.username,)).fetchone():
            return JSONResponse(
                status_code=409,
                content={"code": "ERR_CONFLICT", "message": "用户名已存在", "detail": None},
            )
        # 检查邮箱重复
        if conn.execute("SELECT 1 FROM users WHERE email = ?", (body.email,)).fetchone():
            return JSONResponse(
                status_code=409,
                content={"code": "ERR_CONFLICT", "message": "邮箱已注册", "detail": None},
            )

        user_id = f"u_{uuid.uuid4().hex[:13]}"
        created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        password_hash = hash_password(body.password)

        conn.execute(
            "INSERT INTO users (id, username, email, password_hash, created_at) VALUES (?,?,?,?,?)",
            (user_id, body.username, body.email, password_hash, created_at),
        )

    return RegisterResponse(
        user_id=user_id,
        username=body.username,
        email=body.email,
        created_at=created_at,
    )


@router.post(
    "/login",
    response_model=LoginResponse,
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def login(body: LoginRequest):
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, username, password_hash, is_active FROM users "
            "WHERE username = ? OR email = ?",
            (body.username, body.username),
        ).fetchone()

    if row is None or not verify_password(body.password, row["password_hash"]):
        return JSONResponse(
            status_code=401,
            content={"code": "ERR_UNAUTHORIZED", "message": "用户名或密码错误", "detail": None},
        )

    if not row["is_active"]:
        return JSONResponse(
            status_code=403,
            content={"code": "ERR_FORBIDDEN", "message": "账户已禁用", "detail": None},
        )

    token = create_access_token(row["id"], row["username"])
    return LoginResponse(access_token=token, expires_in=TOKEN_EXPIRES_IN)
