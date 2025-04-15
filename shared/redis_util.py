"""
shared/redis_util.py

Redis工具类模块。

【模块职责】
- 提供Redis连接、发布与订阅的统一接口
- 支持主节点发布、从节点订阅消息
- 支持频道管理、消息压缩（可选）
- 便于后续扩展为异步/高性能实现

【与主/从程序集成点】
- 由 master/app.py、slave/app.py 调用，实现消息同步
- 建议封装为类或函数，便于复用和测试

【与FastAPI集成点】
- 可作为依赖注入，供API路由实现消息发布/订阅等操作

# 下面为Redis工具开发预留区
# def get_redis_client():
#     ...
"""