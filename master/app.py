"""
master/app.py

主节点主程序：定时采集天气数据，写入MySQL并发布到Redis，同时提供健康检查API。

环境依赖说明：
- API_KEY、MySQL地址、Redis地址、经纬度等敏感信息请通过环境变量设置，切勿硬编码在代码中。
- 经纬度参数（WEATHER_LAT, WEATHER_LON）请参考 openweathermap 官方文档设置。

"""

import os
import time
import logging
from threading import Thread
from datetime import UTC, datetime

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
import uvicorn

# 更新导入语句
from shared.db_connector import get_db_connection # 这个仍然需要，因为 mysql_writer 内部使用了它
from shared.redis_util import get_redis_client
from master.weather_api import fetch_weather_by_coords # 使用新模块名
from master.mysql_writer import save_to_mysql # 使用新模块名
from master.redispub import publish_to_redis

app = FastAPI()


@app.get("/api/health")
def health_check():
    """健康检查API，返回服务状态"""
    return {"status": "ok"}


# 日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# 配置读取
API_KEY = os.getenv("WEATHER_API_KEY")
LAT = os.getenv("WEATHER_LAT")
LON = os.getenv("WEATHER_LON")
REDIS_CHANNEL = os.getenv("REDIS_CHANNEL", "weather:updates")

# MySQL连接参数说明
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB", "weather")

# Redis连接参数说明
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


def main_loop():
    """主循环：定时采集、存储、发布"""
    while True:
        # 使用新的 fetch_weather_by_coords 函数
        weather = fetch_weather_by_coords(LAT, LON, API_KEY)
        if weather:
            print(f"采集到天气信息: {weather}")
            # 使用新的 save_to_mysql 和 publish_to_redis 函数
            save_to_mysql(weather, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
            publish_to_redis(weather, REDIS_HOST, REDIS_PORT, REDIS_CHANNEL)
        time.sleep(60)  # 每60秒采集一次


if __name__ == "__main__":
    # 启动定时采集线程
    t = Thread(target=main_loop, daemon=True)
    t.start()
    # 启动FastAPI服务（默认127.0.0.0:8000）
    uvicorn.run(app, host="0.0.0.0", port=8000)