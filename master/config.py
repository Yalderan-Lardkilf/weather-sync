"""
master/config.py

主节点配置文件。

【模块职责】
- 存放API密钥、Redis/MySQL连接等配置信息
- 推荐通过环境变量读取敏感信息（如API密钥、数据库密码等）
- 支持多环境（开发/测试/生产）配置切换

【与主程序集成点】
- 由 master/app.py 导入，统一管理配置
- 可设计为类、字典或pydantic.BaseSettings，便于与FastAPI集成

【与FastAPI集成点】
- 可通过依赖注入，将配置对象传递给API路由和后台任务

# 下面为配置开发预留区
# import os
# API_KEY = os.getenv("WEATHER_API_KEY")
# ...
"""