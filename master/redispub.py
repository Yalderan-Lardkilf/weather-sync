"""
master/redispub.py

处理 Redis 消息发布。
"""

import logging
import json
from shared.redis_util import get_redis_client

def publish_to_redis(weather_data, REDIS_HOST, REDIS_PORT, REDIS_CHANNEL):
    """将天气数据发布到Redis频道"""
    try:
        redis_client = get_redis_client(host=REDIS_HOST, port=REDIS_PORT)
        redis_client.publish(REDIS_CHANNEL, json.dumps(weather_data))
        logging.info(f"数据已发布到Redis频道: {REDIS_CHANNEL}")
        return True
    except Exception as e:
        logging.error(f"Redis发布失败: {e}")
        return False
