"""
首页 Page Object
封装首页的所有元素定位和操作方法
"""
import time
from typing import List, Optional

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):
    """
    首页类
    继承自 BasePage，封装首页相关的所有操作
    """

    SIDEBAR_MENU = (By.CSS_SELECTOR, ".vben-menu, .sidebar-menu, [class*='sidebar']")
    MENU_ITEMS = (By.CSS_SELECTOR, ".vben-menu-item, .vben-sub-menu")
    HEADER = (By.CSS_SELECTOR, "header, .header")
    USER_DROPDOWN = (By.CSS_SELECTOR, ".vben-user-dropdown, [class*='user-dropdown']")
    HOME_URL_PATTERN = "/#/home"

    def __init__(self, driver, base_url: str = ""):
        """
        初始化首页
        
        Args:
            driver: WebDriver 实例
            base_url: 基础 URL
        """
        super().__init__(driver, base_url)

    def is_logged_in(self, timeout: int = 10) -> bool:
        """
        判断是否已登录成功
        通过检查 URL 是否包含 home 路径和侧边栏菜单是否存在
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            是否已登录
        """
        try:
            time.sleep(2)
            current_url = self.driver.current_url
            if "/#/home" in current_url or "/home" in current_url:
                self.logger.info(f"登录成功，当前URL: {current_url}")
                return True

            sidebar = self.driver.find_elements("css selector", "[class*='sidebar'], .vben-menu")
            if sidebar:
                self.logger.info("登录成功，检测到侧边栏菜单")
                return True

            self.logger.warning(f"未检测到登录成功标志，当前URL: {current_url}")
            return False
        except Exception as e:
            self.logger.error(f"检查登录状态失败: {e}")
            return False

    def get_menu_items(self) -> List[str]:
        """
        获取所有菜单项文本
        
        Returns:
            菜单项文本列表
        """
        with allure.step("获取菜单项"):
            elements = self.find_elements(self.MENU_ITEMS)
            return [elem.text for elem in elements if elem.text]

    def click_menu_item(self, menu_name: str):
        """
        点击指定菜单项
        
        Args:
            menu_name: 菜单名称
        """
        with allure.step(f"点击菜单: {menu_name}"):
            locator = (By.XPATH, f"//*[contains(text(), '{menu_name}')]")
            self.click(locator)
            self.logger.info(f"点击菜单: {menu_name}")

    def logout(self):
        """
        退出登录
        """
        with allure.step("退出登录"):
            try:
                self.click(self.USER_DROPDOWN)
                time.sleep(0.5)
                logout_btn = (By.XPATH, "//*[contains(text(), '退出') or contains(text(), '注销')]")
                self.click(logout_btn)
                self.logger.info("退出登录成功")
            except Exception as e:
                self.logger.error(f"退出登录失败: {e}")

    def is_page_loaded(self) -> bool:
        """
        判断首页是否加载完成
        
        Returns:
            页面是否加载完成
        """
        try:
            return self.is_element_present(self.SIDEBAR_MENU)
        except:
            return False
