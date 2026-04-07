"""
登录页面 Page Object
封装登录页面的所有元素定位和操作方法
"""
import time
from typing import Optional, Tuple

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    登录页面类
    继承自 BasePage，封装登录相关的所有操作
    注意：该系统的首页就是登录页面，需要输入机构编码、手机号码、密码三个字段
    """

    ORG_CODE_INPUT = (By.CSS_SELECTOR, "input[placeholder*='机构编码']")
    PHONE_INPUT = (By.CSS_SELECTOR, "input[placeholder*='手机']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder*='密码']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.el-button--primary")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".el-message--error, .el-notification__content")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".el-message--success")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "button:contains('忘记密码')")
    LOGIN_FORM = (By.CSS_SELECTOR, ".el-form")

    def __init__(self, driver, base_url: str = ""):
        """
        初始化登录页面
        
        Args:
            driver: WebDriver 实例
            base_url: 基础 URL
        """
        super().__init__(driver, base_url)
        self.page_url = "/#/auth/login"

    def open_login_page(self):
        """
        打开登录页面（首页就是登录页）
        """
        with allure.step("打开登录页面"):
            self.open(self.page_url)
            self.wait_for_page_load()
            self.logger.info("登录页面已打开")

    def input_org_code(self, org_code: str, delay: float = 0.1):
        """
        输入机构编码（模拟真实用户输入）
        
        Args:
            org_code: 机构编码
            delay: 每个字符输入间隔（秒）
        """
        with allure.step(f"输入机构编码: {org_code}"):
            element = self.wait_for_visible(self.ORG_CODE_INPUT)
            element.clear()
            for char in org_code:
                element.send_keys(char)
                time.sleep(delay)
            self.logger.info(f"输入机构编码: {org_code}")

    def input_phone(self, phone: str, delay: float = 0.1):
        """
        输入手机号码（模拟真实用户输入）
        
        Args:
            phone: 手机号码
            delay: 每个字符输入间隔（秒）
        """
        with allure.step(f"输入手机号码: {phone}"):
            element = self.wait_for_visible(self.PHONE_INPUT)
            element.clear()
            for char in phone:
                element.send_keys(char)
                time.sleep(delay)
            self.logger.info(f"输入手机号码: {phone}")

    def input_password(self, password: str, delay: float = 0.1):
        """
        输入密码（模拟真实用户输入）
        
        Args:
            password: 密码
            delay: 每个字符输入间隔（秒）
        """
        with allure.step("输入密码"):
            element = self.wait_for_visible(self.PASSWORD_INPUT)
            element.clear()
            for char in password:
                element.send_keys(char)
                time.sleep(delay)
            self.logger.info("输入密码完成")

    def click_login_button(self):
        """
        点击登录按钮
        """
        with allure.step("点击登录按钮"):
            self.click(self.LOGIN_BUTTON)
            time.sleep(1)

    def login(self, org_code: str, phone: str, password: str, input_delay: float = 0.1):
        """
        执行登录操作
        
        Args:
            org_code: 机构编码
            phone: 手机号码
            password: 密码
            input_delay: 输入延迟（秒）
        """
        with allure.step(f"使用手机号 '{phone}' 登录"):
            self.input_org_code(org_code, input_delay)
            time.sleep(0.3)
            self.input_phone(phone, input_delay)
            time.sleep(0.3)
            self.input_password(password, input_delay)
            time.sleep(0.5)
            self.click_login_button()
            self.logger.info(f"登录操作完成: {phone}")

    def get_error_message(self) -> str:
        """
        获取错误提示信息
        
        Returns:
            错误提示文本
        """
        try:
            return self.get_text(self.ERROR_MESSAGE, timeout=5)
        except Exception:
            return ""

    def get_success_message(self) -> str:
        """
        获取成功提示信息
        
        Returns:
            成功提示文本
        """
        try:
            return self.get_text(self.SUCCESS_MESSAGE, timeout=5)
        except Exception:
            return ""

    def is_login_successful(self) -> bool:
        """
        判断登录是否成功
        通过检查页面URL是否变化或登录表单是否消失来判断
        
        Returns:
            登录是否成功
        """
        try:
            current_url = self.get_current_url()
            is_on_login_page = "/auth/login" in current_url.lower()
            has_error = self.is_displayed(self.ERROR_MESSAGE, timeout=2)
            return not is_on_login_page and not has_error
        except Exception:
            return False

    def is_login_button_enabled(self) -> bool:
        """
        判断登录按钮是否可用
        
        Returns:
            登录按钮是否可用
        """
        return self.is_enabled(self.LOGIN_BUTTON)

    def click_forgot_password(self):
        """
        点击忘记密码链接
        """
        with allure.step("点击忘记密码链接"):
            self.click(self.FORGOT_PASSWORD_LINK)

    def clear_org_code(self):
        """
        清空机构编码输入框
        """
        self.input_text(self.ORG_CODE_INPUT, "", clear_first=True)

    def clear_phone(self):
        """
        清空手机号码输入框
        """
        self.input_text(self.PHONE_INPUT, "", clear_first=True)

    def clear_password(self):
        """
        清空密码输入框
        """
        self.input_text(self.PASSWORD_INPUT, "", clear_first=True)

    def clear_login_form(self):
        """
        清空登录表单
        """
        with allure.step("清空登录表单"):
            self.clear_org_code()
            self.clear_phone()
            self.clear_password()

    def wait_for_login_page_load(self):
        """
        等待登录页面加载完成
        """
        self.wait_for_visible(self.LOGIN_FORM)
        self.wait_for_visible(self.ORG_CODE_INPUT)
        self.wait_for_visible(self.PHONE_INPUT)
        self.wait_for_visible(self.PASSWORD_INPUT)
        self.wait_for_visible(self.LOGIN_BUTTON)
        self.logger.info("登录页面元素加载完成")

    def verify_login_page_elements(self) -> bool:
        """
        验证登录页面关键元素是否存在
        
        Returns:
            所有关键元素是否都存在
        """
        with allure.step("验证登录页面元素"):
            elements_ok = True
            elements_ok &= self.is_displayed(self.ORG_CODE_INPUT, timeout=5)
            elements_ok &= self.is_displayed(self.PHONE_INPUT, timeout=5)
            elements_ok &= self.is_displayed(self.PASSWORD_INPUT, timeout=5)
            elements_ok &= self.is_displayed(self.LOGIN_BUTTON, timeout=5)
            self.logger.info(f"登录页面元素验证结果: {elements_ok}")
            return elements_ok

    def get_org_code_value(self) -> str:
        """
        获取机构编码输入框的值
        
        Returns:
            机构编码输入框的值
        """
        return self.get_value(self.ORG_CODE_INPUT)

    def get_phone_value(self) -> str:
        """
        获取手机号码输入框的值
        
        Returns:
            手机号码输入框的值
        """
        return self.get_value(self.PHONE_INPUT)

    def get_password_value(self) -> str:
        """
        获取密码输入框的值
        
        Returns:
            密码输入框的值
        """
        return self.get_value(self.PASSWORD_INPUT)
