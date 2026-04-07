"""
日志工具模块
提供统一的日志记录功能，支持控制台输出和文件输出
"""
import logging
import os
from datetime import datetime
from typing import Optional


class Logger:
    """
    日志管理类
    单例模式，确保全局使用同一个日志实例
    """
    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls, name: str = "XiaoEnTest"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(name)
        return cls._instance

    def _initialize(self, name: str):
        """
        初始化日志配置
        
        Args:
            name: 日志名称
        """
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

        if self._logger.handlers:
            return

        log_format = "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s"
        formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)

        log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
        log_filepath = os.path.join(log_dir, log_filename)

        file_handler = logging.FileHandler(log_filepath, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    def debug(self, message: str):
        self._logger.debug(message)

    def info(self, message: str):
        self._logger.info(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def error(self, message: str):
        self._logger.error(message)

    def critical(self, message: str):
        self._logger.critical(message)


def get_logger(name: str = "XiaoEnTest") -> Logger:
    """
    获取日志实例的工厂函数
    
    Args:
        name: 日志名称
        
    Returns:
        Logger实例
    """
    return Logger(name)
