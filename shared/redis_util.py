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

依赖说明：
- 需先安装 redis 库
- 连接参数（host, port）请通过环境变量或配置文件传递，切勿硬编码敏感信息

"""

import redis

def get_redis_client(host, port):
    """
    获取Redis客户端
    参数说明：
        host: Redis地址（如"127.0.0.1"或远程IP）
        port: Redis端口（默认6379）
    返回：
        redis.Redis 对象
    """
    return redis.Redis(host=host, port=port, decode_responses=True)