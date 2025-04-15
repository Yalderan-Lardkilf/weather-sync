"""
master/weather_api.py

OpenWeatherMap API 接口封装，提供天气数据查询功能。
"""

import os
import requests
from typing import Optional, Dict, List

class WeatherAPI:
    """
    OpenWeatherMap API 封装类，提供各种天气数据查询功能。
    """
    
    BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"
    
    def __init__(self, api_key: str = None):
        """
        初始化 WeatherAPI
        
        参数:
            api_key: OpenWeatherMap API key，如果为None则从环境变量获取
        """
        self.api_key = api_key or os.getenv("WEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in WEATHER_API_KEY environment variable")

    def get_weather_data(self, lat: float, lon: float, exclude: List[str] = None, 
                        units: str = "metric", lang: str = "zh_cn") -> Dict:
        """
        获取综合天气数据
        
        参数:
            lat: 纬度
            lon: 经度
            exclude: 要排除的数据部分(current,minutely,hourly,daily,alerts)
            units: 单位制(metric/imperial/standard)
            lang: 语言代码
            
        返回:
            天气数据字典
        """
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
        }
        import urllib.parse
        encoded_params = urllib.parse.urlencode(params)
        response = requests.get(f"{self.BASE_URL}?{encoded_params}")
        response.raise_for_status()
        return response.json()

    def get_current_weather(self, lat: float, lon: float, 
                          units: str = "metric", lang: str = "zh_cn") -> Dict:
        """
        获取当前天气数据
        
        参数:
            lat: 纬度
            lon: 经度
            units: 单位制
            lang: 语言代码
            
        返回:
            当前天气数据
        """
        data = self.get_weather_data(lat, lon,
                                    exclude=["minutely", "hourly", "daily", "alerts"],
                                    units=units, lang=lang)
        return data["current"]

    def get_minutely_forecast(self, lat: float, lon: float, 
                            units: str = "metric", lang: str = "zh_cn") -> List[Dict]:
        """
        获取分钟级降水预报
        
        参数:
            lat: 纬度
            lon: 经度
            units: 单位制
            lang: 语言代码
            
        返回:
            分钟级降水预报列表
        """
        data = self.get_weather_data(lat, lon, 
                                   exclude=["current", "hourly", "daily", "alerts"],
                                   units=units, lang=lang)
        return data["minutely"]

    def get_hourly_forecast(self, lat: float, lon: float, 
                          units: str = "metric", lang: str = "zh_cn") -> List[Dict]:
        """
        获取小时级天气预报
        
        参数:
            lat: 纬度
            lon: 经度
            units: 单位制
            lang: 语言代码
            
        返回:
            小时级天气预报列表
        """
        data = self.get_weather_data(lat, lon, 
                                   exclude=["current", "minutely", "daily", "alerts"],
                                   units=units, lang=lang)
        return data["hourly"]

    def get_daily_forecast(self, lat: float, lon: float, 
                         units: str = "metric", lang: str = "zh_cn") -> List[Dict]:
        """
        获取每日天气预报
        
        参数:
            lat: 纬度
            lon: 经度
            units: 单位制
            lang: 语言代码
            
        返回:
            每日天气预报列表
        """
        data = self.get_weather_data(lat, lon, 
                                   exclude=["current", "minutely", "hourly", "alerts"],
                                   units=units, lang=lang)
        return data["daily"]

    def get_weather_alerts(self, lat: float, lon: float, 
                         units: str = "metric", lang: str = "zh_cn") -> List[Dict]:
        """
        获取天气警报
        
        参数:
            lat: 纬度
            lon: 经度
            units: 单位制
            lang: 语言代码
            
        返回:
            天气警报列表
        """
        data = self.get_weather_data(lat, lon, 
                                   exclude=["current", "minutely", "hourly", "daily"],
                                   units=units, lang=lang)
        return data.get("alerts", [])

    @staticmethod
    def format_temperature(temp: float, units: str) -> str:
        """
        格式化温度显示
        
        参数:
            temp: 温度值
            units: 单位制
            
        返回:
            格式化后的温度字符串
        """
        if units == "metric":
            return f"{temp}°C"
        elif units == "imperial":
            return f"{temp}°F"
        else:
            return f"{temp}K"