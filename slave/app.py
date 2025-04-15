"""
slave/app.py

从节点主程序：订阅Redis频道，实时同步天气数据并本地持久化，同时提供健康检查API。

环境依赖说明：
- Redis地址、频道名等敏感信息请通过环境变量或配置文件设置，切勿硬编码在代码中。
- 本地持久化采用SQLite，数据库文件名可通过环境变量指定。

"""

import os
import json
import logging
import sqlite3
from threading import Thread
from fastapi import FastAPI
import uvicorn

from shared.redis_util import get_redis_client
from slave.data_processor import process_weather_data  # 需在data_processor.py实现

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# FastAPI 健康检查API
app = FastAPI()

@app.get("/api/health")
def health_check():
    """健康检查API，返回服务状态"""
    return {"status": "ok"}

# 配置读取
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_CHANNEL = os.getenv("REDIS_CHANNEL", "weather:updates")
SQLITE_DB = os.getenv("SQLITE_DB", "weather_slave.db")

def init_sqlite():
    """初始化本地SQLite数据库，创建表结构"""
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL,
        lat REAL,
        lon REAL,
        temperature REAL,
        humidity INTEGER,
        weather TEXT,
        recorded_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_to_sqlite(weather_data):
    """将天气数据写入本地SQLite数据库"""
    try:
        conn = sqlite3.connect(SQLITE_DB)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO weather_data (city, lat, lon, temperature, humidity, weather, recorded_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            weather_data["city"],
            weather_data["lat"],
            weather_data["lon"],
            weather_data["temp"],
            weather_data["humidity"],
            weather_data["weather"],
            weather_data["timestamp"]
        ))
        conn.commit()
        conn.close()
        logging.info("数据已本地持久化到SQLite")
    except Exception as e:
        logging.error(f"本地持久化失败: {e}")

def subscribe_loop():
    """订阅Redis频道，处理并本地存储数据"""
    init_sqlite()
    redis_client = get_redis_client(REDIS_HOST, REDIS_PORT)
    pubsub = redis_client.pubsub()
    pubsub.subscribe(REDIS_CHANNEL)
    logging.info(f"已订阅Redis频道: {REDIS_CHANNEL}")

    for message in pubsub.listen():
        if message["type"] == "message":
            try:
                data = json.loads(message["data"])
                # 可在此处调用数据处理逻辑
                processed = process_weather_data(data)
                save_to_sqlite(processed)
            except Exception as e:
                logging.error(f"数据处理或存储异常: {e}")

if __name__ == "__main__":
    # 启动订阅线程
    t = Thread(target=subscribe_loop, daemon=True)
    t.start()
    # 启动FastAPI服务（默认127.0.0.1:8001）
    uvicorn.run(app, host="0.0.0.0", port=8001)