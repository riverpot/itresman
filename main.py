"""
针对传统物理机模式部署IT系统资源利用率低、部署周期长、无有效资源回收机制、
缺乏自动化等挑战，提出一种基于云计算的企业IT资产自动分配系统。系统通过整合
云计算平台，实现虚拟机、云硬盘及虚拟网络等资源的全生命周期管理，核心功能
包括：企业用户管理、虚拟机申请，申请单管理，虚拟机生成，虚拟硬盘生成，虚拟机
挂载硬盘，虚拟网络开通，虚拟机开关机，虚拟机、虚拟硬盘退订，虚拟机销毁等）、
多维度监控。
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from database import init_db
from routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="基于云计算的企业IT资源管理系统",
    description="基于云计算的企业IT资源管理系统",
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {"loc": e["loc"], "msg": e["msg"], "type": e["type"]}
        for e in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"code": "ERR_VALIDATION", "message": "请求参数校验失败", "detail": errors},
    )

app.include_router(auth.router)


@app.get("/")
async def read_root():
    return {"message": "Hello ! 欢迎进入基于云计算的企业IT资源管理系统"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "健康检查"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
