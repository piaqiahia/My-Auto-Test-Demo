import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name): # 定义函数，接收一个 name（通常传入 __name__，便于区分模块来源）
    """
    获取日志器实例

    Args:
        name: 日志器名称（通常使用 __name__）

    Returns:
        logging.Logger: 配置好的日志器
    """

    logger = logging.getLogger(name) # 获取或创建名为 name 的 Logger 实例
    logger.setLevel(logging.DEBUG) # 设置日志器的 最低捕获级别为 DEBUG，确保所有日志（包括调试信息）都能被处理（但是否输出取决于 handler 的级别）

    if not logger.handlers: # 检查该 logger 是否已绑定过 handler 如果没有，才进行后续配置。避免多次调用时重复添加 handler（否则每调用一次，日志就会多输出一遍）
        os.makedirs("logs", exist_ok = True)

        # Python 的 logging 模块采用 Logger → Handler → Output 的结构 必须添加handler指定输出位置
        console_handler = logging.StreamHandler() # 创建控制台输出处理器（默认输出到 sys.stderr）
        console_handler.setLevel(logging.INFO) # 设置其只处理 INFO 及以上级别的日志

        file_handler = RotatingFileHandler( # 创建轮转文件处理器
            "logs/app.log", # 主日志文件路径：logs/app.log
            maxBytes = 5 * 1024 * 1024, # 当文件超过 5MB 时，自动重命名当前文件为 .1，新建 app.log
            backupCount = 3, # 最多保留 3 个旧文件（.1, .2, .3），更早的会被删除
            encoding = "utf-8"
        )

        # 定义统一的日志格式 %(asctime)s：自动生成的时间戳（格式可自定义，默认含毫秒）%(name)s：logger 的名字（即传入的 name）
        # %(levelname)s：日志级别（如 DEBUG, INFO） %(message)s：实际日志内容

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # 将格式器应用到两个处理器上
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # 将两个处理器绑定到 logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger # logger被调用会同时在终端和日志打出同样内容 因为绑定了两个