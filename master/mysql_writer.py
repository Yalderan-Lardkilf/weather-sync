"""
master/mysql_writer.py

处理 MySQL 数据库数据写入。
"""

import logging
from shared.db_connector import get_db_connection

def save_to_mysql(weather_data, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB):
    """将天气数据写入MySQL"""
    try:
        conn = get_db_connection(
            host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB
        )
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO weather_data (city, temperature, humidity, recorded_at, lat, lon, weather)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                sql,
                (
                    weather_data.get("city", ""),
                    weather_data["temp"],
                    weather_data["humidity"],
                    weather_data["timestamp"],
                    weather_data["lat"],
                    weather_data["lon"],
                    weather_data.get("weather", ""),
                ),
            )
        conn.commit()
        conn.close()
        logging.info("数据已写入MySQL")
        return True
    except Exception as e:
        logging.error(f"MySQL写入失败: {e}")
        return False