"""
master/mysql_writer.py

处理 MySQL 数据库数据写入。
"""

import logging
from shared.db_connector import get_db_connection

def save_to_mysql(weather_data, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB):
    """将当前天气数据写入MySQL"""
    try:
        conn = get_db_connection(
            host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB
        )
        with conn.cursor() as cursor:
            # 创建表如果不存在
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_current (
                id INT AUTO_INCREMENT PRIMARY KEY,
                dt INT,
                sunrise INT,
                sunset INT,
                temp FLOAT,
                feels_like FLOAT,
                pressure INT,
                humidity INT,
                dew_point FLOAT,
                uvi FLOAT,
                clouds INT,
                visibility INT,
                wind_speed FLOAT,
                wind_deg INT,
                wind_gust FLOAT,
                weather_id INT,
                weather_main VARCHAR(255),
                weather_description VARCHAR(255),
                weather_icon VARCHAR(255)
            )
            """)

            sql = """
            INSERT INTO weather_current (dt, sunrise, sunset, temp, feels_like, pressure, humidity, dew_point, uvi, clouds, visibility, wind_speed, wind_deg, wind_gust, weather_id, weather_main, weather_description, weather_icon)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            current = weather_data["current"]
            weather = current["weather"][0]
            cursor.execute(
                sql,
                (
                    current["dt"],
                    current["sunrise"],
                    current["sunset"],
                    current["temp"],
                    current["feels_like"],
                    current["pressure"],
                    current["humidity"],
                    current["dew_point"],
                    current["uvi"],
                    current["clouds"],
                    current["visibility"],
                    current["wind_speed"],
                    current["wind_deg"],
                    current["wind_gust"],
                    weather["id"],
                    weather["main"],
                    weather["description"],
                    weather["icon"],
                ),
            )
        conn.commit()
        conn.close()
        logging.info("当前天气数据已写入MySQL")
        return True
    except Exception as e:
        logging.error(f"MySQL写入失败: {e}")
        return False