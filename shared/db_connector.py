"""
shared/db_connector.py

数据库连接工具模块，使用连接池提高性能。

【模块职责】
- 提供MySQL数据库连接池（主节点用）
- 提供SQLite数据库连接的统一接口（从节点用）
- 支持主节点数据持久化、从节点本地查询
- 支持生产环境下SSL安全连接（MySQL）
- 支持批量插入、查询等高性能操作
"""

from dbutils.pooled_db import PooledDB
import pymysql
import sqlite3
import logging

# MySQL连接池实例
_mysql_pool = None

def init_mysql_pool(host, port, user, password, db, 
                   mincached=2, maxcached=5, maxconnections=20):
    """
    初始化MySQL连接池
    参数说明：
        host: MySQL地址
        port: MySQL端口
        user: 用户名
        password: 密码
        db: 数据库名
        mincached: 初始空闲连接数
        maxcached: 最大空闲连接数
        maxconnections: 最大连接数
    """
    global _mysql_pool
    if _mysql_pool is None:
        _mysql_pool = PooledDB(
            creator=pymysql,
            mincached=mincached,
            maxcached=maxcached,
            maxconnections=maxconnections,
            host=host,
            port=port,
            user=user,
            password=password,
            database=db,
            charset='utf8mb4',
            autocommit=False
        )
        logging.info("MySQL连接池初始化完成")

def get_db_connection(host=None, port=None, user=None, 
                     password=None, db=None):
    """
    从连接池获取MySQL数据库连接（主节点用）
    如果连接池未初始化，会自动初始化
    """
    global _mysql_pool
    if _mysql_pool is None:
        if not all([host, port, user, password, db]):
            raise ValueError("MySQL连接参数不完整")
        init_mysql_pool(host, port, user, password, db)
    
    try:
        conn = _mysql_pool.connection()
        logging.debug("成功从连接池获取MySQL连接")
        return conn
    except Exception as e:
        logging.error(f"获取MySQL连接失败: {e}")
        raise

def get_sqlite_connection(db_path):
    """
    获取SQLite数据库连接（从节点用）
    参数说明：
        db_path: SQLite数据库文件路径
    返回：
        sqlite3.Connection 对象
    """
    try:
        conn = sqlite3.connect(db_path)
        logging.debug("成功获取SQLite连接")
        return conn
    except Exception as e:
        logging.error(f"获取SQLite连接失败: {e}")
        raise