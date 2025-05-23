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
from master.weather_api import WeatherAPI
from shared.weather_dao import CurrentWeatherDAO, MinutelyForecastDAO, HourlyForecastDAO, DailyForecastDAO, WeatherAlertsDAO
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

# 初始化MySQL连接池
from shared.db_connector import init_mysql_pool
init_mysql_pool(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    db=MYSQL_DB,
    mincached=2,
    maxcached=5,
    maxconnections=20
)

# Redis连接参数说明
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# 实例化 DAO
current_weather_dao = CurrentWeatherDAO(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
minutely_forecast_dao = MinutelyForecastDAO(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
hourly_forecast_dao = HourlyForecastDAO(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
daily_forecast_dao = DailyForecastDAO(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
weather_alerts_dao = WeatherAlertsDAO(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)

# 实例化 WeatherAPI
weather_api = WeatherAPI(API_KEY)


def main_loop():
    """主循环：定时采集、存储、发布"""
    while True:
        # 使用新的 fetch_weather_by_coords 函数
        try:
            logging.info("开始采集天气数据...")
            weather_data = weather_api.get_weather_data(float(LAT), float(LON))
            current_weather = weather_data["current"]
            minutely_forecast = weather_data.get("minutely", [])
            hourly_forecast = weather_data["hourly"]
            daily_forecast = weather_data["daily"]
            alerts = weather_data.get("alerts", [])
            logging.info("天气数据采集完成。")

            if current_weather:
                logging.info("开始保存当前天气数据...")
                current_weather_dao.insert(current_weather)
                logging.info("当前天气数据已保存。")
            if minutely_forecast:
                logging.info("开始保存分钟级天气数据...")
                minutely_forecast_dao.insert(minutely_forecast)
                logging.info("分钟级天气数据已保存。")
            if hourly_forecast:
                logging.info("开始保存小时级天气数据...")
                hourly_forecast_dao.insert(hourly_forecast)
                logging.info("小时级天气数据已保存。")
            if daily_forecast:
                logging.info("开始保存每日天气数据...")
                daily_forecast_dao.insert(daily_forecast)
                logging.info("每日天气数据已保存。")
            if alerts:
                logging.info("开始保存天气警报数据...")
                weather_alerts_dao.insert(alerts)
                logging.info("天气警报数据已保存。")

            logging.info("开始发布天气数据到Redis...")
            publish_to_redis(weather_data, REDIS_HOST, REDIS_PORT, REDIS_CHANNEL)
            logging.info("天气数据已发布到Redis。")
        except Exception as e:
            logging.error(f"采集或存储天气数据失败: {e}")
        time.sleep(60)  # 每60秒采集一次


if __name__ == "__main__":
    # 启动定时采集线程
    t = Thread(target=main_loop, daemon=True)
    t.start()
    # 启动FastAPI服务（默认127.0.0.0:8000）
    uvicorn.run(app, host="0.0.0.0", port=8000)