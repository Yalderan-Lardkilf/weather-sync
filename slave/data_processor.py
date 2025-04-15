"""
slave/data_processor.py

从节点数据处理模块。

【模块职责】
- 处理和转换接收到的天气数据（如JSON解析、单位转换等）
- 数据校验与清洗，保证数据质量
- 可选：本地持久化（如写入本地数据库或文件）
- 为本地API（如 /api/weather/local）提供数据支持

【与主程序集成点】
- 由 slave/app.py 调用，处理Redis订阅到的数据
- 可设计为类或函数接口，便于扩展和测试

【与FastAPI集成点】
- 可作为依赖注入，为API路由提供数据处理能力

# 下面为数据处理逻辑开发预留区
# def process_weather_data(data):
#     ...
"""