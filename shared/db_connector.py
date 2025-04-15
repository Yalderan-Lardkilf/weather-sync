"""
shared/db_connector.py

数据库连接工具模块。

【模块职责】
- 提供MySQL数据库连接的统一接口（主节点用）
- 提供SQLite数据库连接的统一接口（从节点用）
- 支持主节点数据持久化、从节点本地查询
- 支持生产环境下SSL安全连接（MySQL）
- 支持批量插入、查询等高性能操作

【与主/从程序集成点】
- 由 master/app.py、slave/app.py 调用，进行数据读写
- 建议封装为类或上下文管理器，便于资源管理

【与FastAPI集成点】
- 可作为依赖注入，供API路由直接调用数据库操作

依赖说明：
- 需先安装 pymysql（主节点MySQL）和 sqlite3（Python内置，适用于从节点本地持久化）
- 连接参数请通过环境变量或配置文件传递，切勿硬编码敏感信息

"""

import pymysql
import sqlite3

def get_db_connection(host, port, user, password, db):
    """
    获取MySQL数据库连接（主节点用）
    参数说明：
        host: MySQL地址（如"127.0.0.1"或远程IP）
        port: MySQL端口（默认3306）
        user: 用户名
        password: 密码
        db: 数据库名
    返回：
        pymysql.connections.Connection 对象
    """
    return pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db,
        charset="utf8mb4",
        autocommit=False
        # 如需SSL，可加 ssl={"ca": "..."}
    )

def get_sqlite_connection(db_path):
    """
    获取SQLite数据库连接（从节点用）
    参数说明：
        db_path: SQLite数据库文件路径（如"weather_slave.db"）
    返回：
        sqlite3.Connection 对象
    """
    return sqlite3.connect(db_path)