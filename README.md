# 基于云计算的企业IT资源管理系统

## 项目简介

针对传统物理机模式部署IT系统资源利用率低、部署周期长、无有效资源回收机制、缺乏自动化等挑战，本系统通过整合云计算平台，实现虚拟机、云硬盘及虚拟网络等资源的全生命周期管理。

## 技术栈

| 组件 | 版本 |
|---|---|
| Python | 3.11+ |
| FastAPI | 0.104.1 |
| Uvicorn | 0.24.0 |
| Pydantic | 2.5.0 |

## 快速启动

```bash
# 安装依赖
pip install -r requirements.txt

# 启动开发服务器（热重载）
python main.py

# 或直接用 uvicorn
uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

服务启动后，访问 `http://127.0.0.1:8001/docs` 查看交互式 API 文档。

---

## API 文档

### 用户管理

Base URL：`/api/v1/auth`

---

#### 1. 用户注册

```
POST /api/v1/auth/register
```

**请求体（application/json）**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| username | string | 是 | 用户名，3~32 个字符，唯一 |
| email | string | 是 | 邮箱地址，唯一 |
| password | string | 是 | 密码，8~64 个字符 |
| confirm_password | string | 是 | 确认密码，需与 password 一致 |

**请求示例**

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "P@ssw0rd123",
  "confirm_password": "P@ssw0rd123"
}
```

**成功响应 `201 Created`**

```json
{
  "user_id": "u_01HX3K9ABCDEF",
  "username": "alice",
  "email": "alice@example.com",
  "created_at": "2026-04-17T08:00:00Z"
}
```

**异常流程**

| 场景 | HTTP 状态码 | 业务错误码 |
|---|---|---|
| 用户名已存在 | 409 | ERR_CONFLICT |
| 邮箱已注册 | 409 | ERR_CONFLICT |
| 两次密码不一致 | 422 | ERR_VALIDATION |
| 参数格式不合法 | 422 | ERR_VALIDATION |

---

#### 2. 用户登录

```
POST /api/v1/auth/login
```

**请求体（application/json）**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| username | string | 是 | 用户名或邮箱地址 |
| password | string | 是 | 密码 |

**请求示例**

```json
{
  "username": "alice",
  "password": "P@ssw0rd123"
}
```

**成功响应 `200 OK`**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

> `expires_in` 单位为秒，默认 86400（24 小时）。

**异常流程**

| 场景 | HTTP 状态码 | 业务错误码 |
|---|---|---|
| 用户名或密码错误 | 401 | ERR_UNAUTHORIZED |
| 账户已禁用 | 403 | ERR_FORBIDDEN |
| 参数格式不合法 | 422 | ERR_VALIDATION |

---

#### 3. 用户登出

```
POST /api/v1/auth/logout
```

**请求头**

| 字段 | 必填 | 说明 |
|---|---|---|
| Authorization | 是 | `Bearer <access_token>` |

**请求示例**

```http
POST /api/v1/auth/logout HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**成功响应 `200 OK`**

```json
{
  "message": "登出成功"
}
```

**异常流程**

| 场景 | HTTP 状态码 | 业务错误码 |
|---|---|---|
| Token 无效 | 401 | ERR_UNAUTHORIZED |
| Token 已过期 | 401 | ERR_UNAUTHORIZED |

---

#### 4. 修改密码

```
PUT /api/v1/auth/password
```

**请求头**

| 字段 | 必填 | 说明 |
|---|---|---|
| Authorization | 是 | `Bearer <access_token>` |

**请求体（application/json）**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| old_password | string | 是 | 当前密码 |
| new_password | string | 是 | 新密码，8~64 个字符 |
| confirm_new_password | string | 是 | 确认新密码，需与 new_password 一致 |

**请求示例**

```json
{
  "old_password": "P@ssw0rd123",
  "new_password": "NewP@ss456!",
  "confirm_new_password": "NewP@ss456!"
}
```

**成功响应 `200 OK`**

```json
{
  "message": "密码修改成功"
}
```

**异常流程**

| 场景 | HTTP 状态码 | 业务错误码 |
|---|---|---|
| 旧密码错误 | 400 | ERR_WRONG_OLD_PWD |
| 新旧密码相同 | 422 | ERR_VALIDATION |
| 两次新密码不一致 | 422 | ERR_VALIDATION |
| Token 无效或已过期 | 401 | ERR_UNAUTHORIZED |

---

## 错误码说明

所有错误响应统一格式如下：

```json
{
  "code": "ERR_UNAUTHORIZED",
  "message": "Token 无效或已过期",
  "detail": null
}
```

| HTTP 状态码 | 业务错误码 | 说明 |
|---|---|---|
| 400 | ERR_WRONG_OLD_PWD | 旧密码错误 |
| 401 | ERR_UNAUTHORIZED | Token 无效、已过期或未登录 |
| 403 | ERR_FORBIDDEN | 账户已禁用，无权限访问 |
| 409 | ERR_CONFLICT | 用户名或邮箱已存在 |
| 422 | ERR_VALIDATION | 请求参数校验失败 |
| 500 | ERR_INTERNAL | 服务器内部错误 |
