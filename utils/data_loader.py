"""
数据加载工具模块
支持从 YAML、Excel、CSV、JSON 文件加载测试数据
"""
import json
import os
from typing import Any, Dict, List, Optional, Union

import yaml


class DataLoader:
    """
    数据加载器类
    提供多种格式测试数据的加载功能
    """

    def __init__(self, data_dir: Optional[str] = None):
        """
        初始化数据加载器
        
        Args:
            data_dir: 数据文件目录，默认为项目根目录下的 data 文件夹
        """
        if data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        else:
            self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """
        加载 YAML 格式文件
        
        Args:
            filename: 文件名（相对于 data 目录）
            
        Returns:
            解析后的字典数据
        """
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def load_json(self, filename: str) -> Union[Dict[str, Any], List[Any]]:
        """
        加载 JSON 格式文件
        
        Args:
            filename: 文件名（相对于 data 目录）
            
        Returns:
            解析后的字典或列表数据
        """
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_excel(self, filename: str, sheet_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        加载 Excel 文件数据
        
        Args:
            filename: 文件名（相对于 data 目录）
            sheet_name: 工作表名称，默认为第一个工作表
            
        Returns:
            每行数据转换为字典的列表
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("请安装 pandas 和 openpyxl: pip install pandas openpyxl")

        filepath = os.path.join(self.data_dir, filename)
        df = pd.read_excel(filepath, sheet_name=sheet_name or 0)
        return df.to_dict(orient="records")

    def load_csv(self, filename: str) -> List[Dict[str, Any]]:
        """
        加载 CSV 文件数据
        
        Args:
            filename: 文件名（相对于 data 目录）
            
        Returns:
            每行数据转换为字典的列表
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("请安装 pandas: pip install pandas")

        filepath = os.path.join(self.data_dir, filename)
        df = pd.read_csv(filepath, encoding="utf-8")
        return df.to_dict(orient="records")


class ConfigLoader:
    """
    配置加载器类
    专门用于加载项目配置文件
    """

    _config: Optional[Dict[str, Any]] = None

    @classmethod
    def load_config(cls, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径，默认为 config/config.yaml
            
        Returns:
            配置字典
        """
        if cls._config is not None:
            return cls._config

        if config_path is None:
            project_root = os.path.dirname(os.path.dirname(__file__))
            # 优先加载本地配置文件（包含敏感信息）
            local_config_path = os.path.join(project_root, "config", "config.local.yaml")
            # 默认配置文件（不包含敏感信息，用于版本控制）
            default_config_path = os.path.join(project_root, "config", "config.yaml")
            
            # 如果本地配置文件存在，优先使用
            if os.path.exists(local_config_path):
                config_path = local_config_path
            else:
                config_path = default_config_path

        with open(config_path, "r", encoding="utf-8") as f:
            cls._config = yaml.safe_load(f)

        return cls._config

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        获取配置项
        
        Args:
            key: 配置键，支持点号分隔的嵌套键，如 "browser.name"
            default: 默认值
            
        Returns:
            配置值
        """
        config = cls.load_config()
        keys = key.split(".")
        value = config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    @classmethod
    def reload(cls, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        重新加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            配置字典
        """
        cls._config = None
        return cls.load_config(config_path)