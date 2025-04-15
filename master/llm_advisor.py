"""
master/llm_advisor.py

大模型对话模块，提供穿衣建议和风险预警。
"""

import os
import logging

class LLMAdvisor:
    """
    大模型对话模块，调用LLM API提供建议。
    """

    def __init__(self):
        """
        初始化LLMAdvisor，从环境变量获取API Key。
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logging.error("OPENAI_API_KEY 未设置")

    def get_advice(self, weather_data):
        """
        根据天气数据获取穿衣建议和风险预警。
        参数：
            weather_data: 天气数据
        返回：
            包含建议和预警的文本
        """
        try:
            # TODO: 调用LLM API，根据天气数据生成建议
            advice = f"根据当前天气，建议穿{weather_data['weather']}的衣服，注意{weather_data['temperature']}度的气温。"
            return advice
        except Exception as e:
            logging.error(f"调用LLM API失败: {e}")
            return "获取建议失败，请稍后重试。"

# 示例调用
if __name__ == "__main__":
    advisor = LLMAdvisor()
    weather_data = {
        "city": "北京",
        "weather": "晴朗",
        "temperature": 25
    }
    advice = advisor.get_advice(weather_data)
    print(advice)