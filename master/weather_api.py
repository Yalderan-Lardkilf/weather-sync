"""
master/weather_api.py

处理不同格式的 OpenWeatherMap API 调用。
"""

import logging
from datetime import datetime, UTC
import requests

# OpenWeatherMap API URL 模板
API_URL_BY_COORDS = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&units=metric"
# 可以根据需要添加其他格式的 URL 模板，例如按城市名查询
# API_URL_BY_CITY = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"

def fetch_weather_by_coords(lat, lon, api_key):
    """
    通过经纬度调用外部天气API，返回标准化天气数据。

    参数:
        lat (str): 纬度
        lon (str): 经度
        api_key (str): OpenWeatherMap API key

    返回:
        dict: 标准化天气数据，包含 timestamp, city, lat, lon, temp, humidity, weather
        None: 获取失败时返回 None
    """
    if not all([lat, lon, api_key]):
        logging.error("获取天气数据失败: 缺少经纬度或 API Key")
        return None

    url = API_URL_BY_COORDS.format(lat=lat, lon=lon, key=api_key)
    try:
        resp = requests.get(url, timeout=10) # 增加超时时间
        resp.raise_for_status() # 检查 HTTP 错误状态码
        data = resp.json()

        # 检查返回数据是否完整
        if "coord" not in data or "main" not in data:
             logging.error(f"API 返回数据不完整: {data}")
             return None

        # 格式化时间为 MySQL 支持的格式
        recorded_at = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")

        return {
            "timestamp": recorded_at,
            "city": data.get("name", f"Coords_{lat}_{lon}"), # 如果没有城市名，用坐标代替
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"] if data.get("weather") else "N/A" # 处理 weather 字段可能不存在的情况
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"获取天气数据网络请求失败: {e}")
        return None
    except Exception as e:
        logging.error(f"处理天气数据时发生未知错误: {e}")
        return None

# 可以根据需要添加其他 fetch 函数，例如按城市名查询
# def fetch_weather_by_city(city, api_key):
#     # ... 实现按城市名查询的逻辑 ...
#     pass