"""
针对传统物理机模式部署IT系统资源利用率低、部署周期长、无有效资源回收机制、
缺乏自动化等挑战，提出一种基于云计算的企业IT资产自动分配系统。系统通过整合
云计算平台，实现虚拟机、云硬盘及虚拟网络等资源的全生命周期管理，核心功能
包括：企业用户管理、虚拟机申请，申请单管理，虚拟机生成，虚拟硬盘生成，虚拟机
挂载硬盘，虚拟网络开通，虚拟机开关机，虚拟机、虚拟硬盘退订，虚拟机销毁等）、
多维度监控。
"""

from fastapi import FastAPI

app = FastAPI(
    title="基于云计算的企业IT资源管理系统",
    description="基于云计算的企业IT资源管理系统",
    version="1.0.0"
)


@app.get("/")
async def read_root():
    """根路径，返回欢迎消息"""
    return {"message": "Hello ! 欢迎进入基于云计算的企业IT资源管理系统"}


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "service": "健康检查"}


if __name__ == "__main__":
    import uvicorn
    # 开发模式启动，支持热重载
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
