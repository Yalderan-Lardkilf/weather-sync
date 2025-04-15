"""
slave/data_processor.py

从节点数据处理模块。

【模块职责】
- 校验和处理接收到的天气数据，保证数据完整性和可用性
- 可扩展单位转换、异常值过滤、字段补全等功能
- 为本地持久化和API展示提供标准化数据

"""

import logging
from datetime import datetime

def process_weather_data(data):
    """
    对接收到的天气数据进行校验、清洗和标准化处理

    参数:
        data: dict，原始天气数据，预期字段包括
            - city: str
            - lat: float
            - lon: float
            - temp: float
            - humidity: int
            - weather: str
            - timestamp: str

    返回:
        dict，处理后的数据，字段同上

    异常:
        若数据不合法，抛出 ValueError
    """
    required_fields = ["city", "lat", "lon", "temp", "humidity", "weather", "timestamp"]
    for field in required_fields:
        if field not in data:
            logging.error(f"缺少字段: {field}")
            raise ValueError(f"缺少字段: {field}")

    # 类型和范围校验
    try:
        city = str(data["city"])
        lat = float(data["lat"])
        lon = float(data["lon"])
        temp = float(data["temp"])
        humidity = int(data["humidity"])
        weather = str(data["weather"])
        # 格式化时间为 MySQL/SQLite 支持的格式
        try:
            # 若已是标准格式则直接用，否则尝试转换
            dt = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
            timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            # 兼容主节点传来的 ISO 格式
            try:
                dt = datetime.fromisoformat(data["timestamp"].replace("Z", ""))
                timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                timestamp = data["timestamp"]  # 保底兜底
    except Exception as e:
        logging.error(f"字段类型转换失败: {e}")
        raise ValueError(f"字段类型转换失败: {e}")

    # 合理性校验（可根据实际需求调整）
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        logging.error(f"经纬度超出范围: lat={lat}, lon={lon}")
        raise ValueError(f"经纬度超出范围: lat={lat}, lon={lon}")
    if not (-100 <= temp <= 100):
        logging.warning(f"温度异常: {temp}")
    if not (0 <= humidity <= 100):
        logging.warning(f"湿度异常: {humidity}")

    # 返回标准化数据
    return {
        "city": city,
        "lat": lat,
        "lon": lon,
        "temp": temp,
        "humidity": humidity,
        "weather": weather,
        "timestamp": timestamp
    }