from pydantic import BaseModel, EmailStr, field_validator, model_validator


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("username")
    @classmethod
    def username_length(cls, v: str) -> str:
        if not 3 <= len(v) <= 32:
            raise ValueError("用户名长度须在 3~32 个字符之间")
        return v

    @field_validator("password")
    @classmethod
    def password_length(cls, v: str) -> str:
        if not 8 <= len(v) <= 64:
            raise ValueError("密码长度须在 8~64 个字符之间")
        return v

    @model_validator(mode="after")
    def passwords_match(self) -> "RegisterRequest":
        if self.password != self.confirm_password:
            raise ValueError("两次输入的密码不一致")
        return self


class RegisterResponse(BaseModel):
    user_id: str
    username: str
    email: str
    created_at: str


class LoginRequest(BaseModel):
    username: str   # 用户名或邮箱
    password: str

    @field_validator("username", "password")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("不能为空")
        return v


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int


class ErrorResponse(BaseModel):
    code: str
    message: str
    detail: object = None
