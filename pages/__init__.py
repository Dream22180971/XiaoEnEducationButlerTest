"""
Page Object 模块初始化文件
"""
from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.login_page import LoginPage

__all__ = [
    "BasePage",
    "LoginPage",
    "HomePage",
]
