"""
基础页面类模块
封装 Selenium WebDriver 的常用操作，提供统一的页面操作接口
所有 Page Object 类都应继承此类
"""
import os
from datetime import datetime
from typing import Any, List, Optional, Tuple, Union

import allure
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from utils.logger import get_logger

logger = get_logger()


class BasePage:
    """
    基础页面类
    封装所有页面共用的操作方法，包括元素定位、等待、点击、输入、截图等
    """

    def __init__(self, driver: WebDriver, base_url: str = ""):
        """
        初始化基础页面类
        
        Args:
            driver: WebDriver 实例
            base_url: 基础 URL
        """
        self.driver = driver
        self.base_url = base_url
        self.timeout = 15
        self.logger = logger

    def open(self, url: str = ""):
        """
        打开页面
        
        Args:
            url: 页面 URL，可以是相对路径或完整 URL
        """
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"
        self.logger.info(f"打开页面: {full_url}")
        self.driver.get(full_url)

    def get_current_url(self) -> str:
        """
        获取当前页面 URL
        
        Returns:
            当前页面 URL
        """
        return self.driver.current_url

    def get_title(self) -> str:
        """
        获取当前页面标题
        
        Returns:
            页面标题
        """
        return self.driver.title

    def find_element(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ) -> WebElement:
        """
        查找单个元素，带显式等待
        
        Args:
            locator: 元素定位器，格式为 (By.XXX, "value")
            timeout: 超时时间（秒），默认使用 self.timeout
            
        Returns:
            WebElement 实例
            
        Raises:
            TimeoutException: 元素未找到时抛出
        """
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.debug(f"找到元素: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"元素未找到: {locator}")
            raise

    def find_elements(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ) -> List[WebElement]:
        """
        查找多个元素，带显式等待
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（秒）
            
        Returns:
            WebElement 列表
        """
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            elements = self.driver.find_elements(*locator)
            self.logger.debug(f"找到 {len(elements)} 个元素: {locator}")
            return elements
        except TimeoutException:
            self.logger.warning(f"元素未找到: {locator}")
            return []

    def wait_for_visible(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ) -> WebElement:
        """
        等待元素可见
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（秒）
            
        Returns:
            可见的 WebElement 实例
        """
        timeout = timeout or self.timeout
        self.logger.debug(f"等待元素可见: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ) -> WebElement:
        """
        等待元素可点击
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（秒）
            
        Returns:
            可点击的 WebElement 实例
        """
        timeout = timeout or self.timeout
        self.logger.debug(f"等待元素可点击: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_invisible(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ) -> bool:
        """
        等待元素不可见（消失）
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（秒）
            
        Returns:
            元素是否已不可见
        """
        timeout = timeout or self.timeout
        self.logger.debug(f"等待元素不可见: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def wait_for_text(
        self,
        locator: Tuple[str, str],
        text: str,
        timeout: Optional[int] = None
    ) -> bool:
        """
        等待元素包含指定文本
        
        Args:
            locator: 元素定位器
            text: 期望的文本
            timeout: 超时时间（秒）
            
        Returns:
            元素是否包含指定文本
        """
        timeout = timeout or self.timeout
        self.logger.debug(f"等待元素文本为 '{text}': {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )

    def click(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None,
        retry_count: int = 3
    ):
        """
        点击元素，支持重试机制
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（秒）
            retry_count: 重试次数
        """
        for attempt in range(retry_count):
            try:
                element = self.wait_for_clickable(locator, timeout)
                element.click()
                self.logger.info(f"点击元素成功: {locator}")
                return
            except (
                ElementClickInterceptedException,
                ElementNotInteractableException,
                StaleElementReferenceException
            ) as e:
                self.logger.warning(f"点击元素失败，尝试 {attempt + 1}/{retry_count}: {str(e)}")
                if attempt == retry_count - 1:
                    self.logger.error(f"点击元素最终失败: {locator}")
                    raise

    def click_by_js(self, locator: Tuple[str, str], timeout: Optional[int] = None):
        """
        使用 JavaScript 点击元素（适用于被遮挡的元素）
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（秒）
        """
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].click();", element)
        self.logger.info(f"JavaScript 点击元素成功: {locator}")

    def input_text(
        self,
        locator: Tuple[str, str],
        text: str,
        clear_first: bool = True,
        timeout: Optional[int] = None
    ):
        """
        在输入框中输入文本
        
        Args:
            locator: 元素定位器
            text: 要输入的文本
            clear_first: 是否先清空输入框
            timeout: 超时时间（秒）
        """
        element = self.wait_for_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        self.logger.info(f"输入文本 '{text}' 到元素: {locator}")

    def input_text_by_js(
        self,
        locator: Tuple[str, str],
        text: str,
        timeout: Optional[int] = None
    ):
        """
        使用 JavaScript 输入文本（适用于特殊场景）
        
        Args:
            locator: 元素定位器
            text: 要输入的文本
            timeout: 超时时间（秒）
        """
        element = self.find_element(locator, timeout)
        self.driver.execute_script(
            "arguments[0].value = arguments[1];", element, text
        )
        self.logger.info(f"JavaScript 输入文本 '{text}' 到元素: {locator}")

    def get_text(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> str:
        """
        获取元素的文本内容
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（秒）
            
        Returns:
            元素的文本内容
        """
        element = self.wait_for_visible(locator, timeout)
        text = element.text
        self.logger.debug(f"获取元素文本: {locator} -> '{text}'")
        return text

    def get_value(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> str:
        """
        获取输入框的 value 属性值
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（秒）
            
        Returns:
            输入框的 value 值
        """
        element = self.find_element(locator, timeout)
        value = element.get_attribute("value")
        self.logger.debug(f"获取元素 value: {locator} -> '{value}'")
        return value

    def get_attribute(
        self,
        locator: Tuple[str, str],
        attribute: str,
        timeout: Optional[int] = None
    ) -> Optional[str]:
        """
        获取元素的指定属性值
        
        Args:
            locator: 元素定位器
            attribute: 属性名
            timeout: 超时时间（秒）
            
        Returns:
            属性值
        """
        element = self.find_element(locator, timeout)
        value = element.get_attribute(attribute)
        self.logger.debug(f"获取元素属性 {attribute}: {locator} -> '{value}'")
        return value

    def is_displayed(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        """
        判断元素是否可见
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（秒）
            
        Returns:
            元素是否可见
        """
        try:
            self.wait_for_visible(locator, timeout or 5)
            return True
        except TimeoutException:
            return False

    def is_enabled(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        """
        判断元素是否可用
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（秒）
            
        Returns:
            元素是否可用
        """
        element = self.find_element(locator, timeout)
        return element.is_enabled()

    def is_selected(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        """
        判断元素是否被选中（用于复选框、单选框）
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（秒）
            
        Returns:
            元素是否被选中
        """
        element = self.find_element(locator, timeout)
        return element.is_selected()

    def select_by_visible_text(
        self,
        locator: Tuple[str, str],
        text: str,
        timeout: Optional[int] = None
    ):
        """
        通过可见文本选择下拉框选项
        
        Args:
            locator: 元素定位器
            text: 选项文本
            timeout: 超时时间（秒）
        """
        element = self.find_element(locator, timeout)
        select = Select(element)
        select.select_by_visible_text(text)
        self.logger.info(f"选择下拉框选项 '{text}': {locator}")

    def select_by_value(
        self,
        locator: Tuple[str, str],
        value: str,
        timeout: Optional[int] = None
    ):
        """
        通过 value 属性选择下拉框选项
        
        Args:
            locator: 元素定位器
            value: 选项的 value 值
            timeout: 超时时间（秒）
        """
        element = self.find_element(locator, timeout)
        select = Select(element)
        select.select_by_value(value)
        self.logger.info(f"选择下拉框选项 value='{value}': {locator}")

    def hover(self, locator: Tuple[str, str], timeout: Optional[int] = None):
        """
        鼠标悬停在元素上
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（秒）
        """
        element = self.find_element(locator, timeout)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.logger.info(f"鼠标悬停在元素上: {locator}")

    def right_click(self, locator: Tuple[str, str], timeout: Optional[int] = None):
        """
        右键点击元素
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（秒）
        """
        element = self.find_element(locator, timeout)
        actions = ActionChains(self.driver)
        actions.context_click(element).perform()
        self.logger.info(f"右键点击元素: {locator}")

    def double_click(self, locator: Tuple[str, str], timeout: Optional[int] = None):
        """
        双击元素
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（秒）
        """
        element = self.find_element(locator, timeout)
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.logger.info(f"双击元素: {locator}")

    def drag_and_drop(
        self,
        source_locator: Tuple[str, str],
        target_locator: Tuple[str, str],
        timeout: Optional[int] = None
    ):
        """
        拖拽元素到目标位置
        
        Args:
            source_locator: 源元素定位器
            target_locator: 目标元素定位器
            timeout: 超时时间（秒）
        """
        source = self.find_element(source_locator, timeout)
        target = self.find_element(target_locator, timeout)
        actions = ActionChains(self.driver)
        actions.drag_and_drop(source, target).perform()
        self.logger.info(f"拖拽元素: {source_locator} -> {target_locator}")

    def press_key(self, locator: Tuple[str, str], key: str, timeout: Optional[int] = None):
        """
        发送键盘按键
        
        Args:
            locator: 元素定位器
            key: 按键名称，如 "ENTER", "TAB", "ESCAPE" 等
            timeout: 超时时间（秒）
        """
        element = self.find_element(locator, timeout)
        key_obj = getattr(Keys, key.upper(), None)
        if key_obj is None:
            raise ValueError(f"无效的按键名称: {key}")
        element.send_keys(key_obj)
        self.logger.info(f"发送按键 {key} 到元素: {locator}")

    def scroll_to_element(self, locator: Tuple[str, str], timeout: Optional[int] = None):
        """
        滚动到指定元素位置
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（秒）
        """
        element = self.find_element(locator, timeout)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )
        self.logger.info(f"滚动到元素位置: {locator}")

    def scroll_to_top(self):
        """
        滚动到页面顶部
        """
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.logger.info("滚动到页面顶部")

    def scroll_to_bottom(self):
        """
        滚动到页面底部
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.logger.info("滚动到页面底部")

    def switch_to_frame(self, locator: Tuple[str, str], timeout: Optional[int] = None):
        """
        切换到 iframe
        
        Args:
            locator: iframe 元素定位器
            timeout: 超时时间（秒）
        """
        WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.frame_to_be_available_and_switch_to_it(locator)
        )
        self.logger.info(f"切换到 iframe: {locator}")

    def switch_to_default_content(self):
        """
        切换回主文档
        """
        self.driver.switch_to.default_content()
        self.logger.info("切换回主文档")

    def switch_to_window(self, window_index: int = -1):
        """
        切换到指定窗口
        
        Args:
            window_index: 窗口索引，-1 表示最新的窗口
        """
        handles = self.driver.window_handles
        if window_index == -1:
            window_index = len(handles) - 1
        self.driver.switch_to.window(handles[window_index])
        self.logger.info(f"切换到窗口 {window_index}")

    def close_current_window(self):
        """
        关闭当前窗口
        """
        self.driver.close()
        self.logger.info("关闭当前窗口")

    def accept_alert(self, timeout: Optional[int] = None):
        """
        接受警告框
        
        Args:
            timeout: 超时时间（秒）
        """
        WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.alert_is_present()
        ).accept()
        self.logger.info("接受警告框")

    def dismiss_alert(self, timeout: Optional[int] = None):
        """
        取消警告框
        
        Args:
            timeout: 超时时间（秒）
        """
        WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.alert_is_present()
        ).dismiss()
        self.logger.info("取消警告框")

    def get_alert_text(self, timeout: Optional[int] = None) -> str:
        """
        获取警告框文本
        
        Args:
            timeout: 超时时间（秒）
            
        Returns:
            警告框文本
        """
        alert = WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.alert_is_present()
        )
        text = alert.text
        self.logger.info(f"获取警告框文本: '{text}'")
        return text

    def take_screenshot(self, filename: Optional[str] = None) -> str:
        """
        截取当前页面截图
        
        Args:
            filename: 截图文件名，不指定则自动生成
            
        Returns:
            截图文件路径
        """
        screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        filepath = os.path.join(screenshot_dir, filename)
        self.driver.save_screenshot(filepath)
        self.logger.info(f"截图已保存: {filepath}")
        return filepath

    def attach_screenshot_to_allure(self, name: str = "页面截图"):
        """
        截图并附加到 Allure 报告
        
        Args:
            name: 截图名称
        """
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
        self.logger.info(f"截图已附加到 Allure 报告: {name}")

    def wait_for_page_load(self, timeout: Optional[int] = None):
        """
        等待页面加载完成
        
        Args:
            timeout: 超时时间（秒）
        """
        timeout = timeout or self.timeout
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        self.logger.info("页面加载完成")

    def execute_script(self, script: str, *args) -> Any:
        """
        执行 JavaScript 脚本
        
        Args:
            script: JavaScript 代码
            *args: 脚本参数
            
        Returns:
            脚本执行结果
        """
        result = self.driver.execute_script(script, *args)
        self.logger.debug(f"执行 JavaScript: {script[:50]}...")
        return result

    def refresh(self):
        """
        刷新当前页面
        """
        self.driver.refresh()
        self.logger.info("页面已刷新")

    def back(self):
        """
        后退到上一页
        """
        self.driver.back()
        self.logger.info("后退到上一页")

    def forward(self):
        """
        前进到下一页
        """
        self.driver.forward()
        self.logger.info("前进到下一页")

    def delete_all_cookies(self):
        """
        删除所有 cookies
        """
        self.driver.delete_all_cookies()
        self.logger.info("已删除所有 cookies")

    def get_cookie(self, name: str) -> Optional[dict]:
        """
        获取指定名称的 cookie
        
        Args:
            name: cookie 名称
            
        Returns:
            cookie 字典
        """
        return self.driver.get_cookie(name)

    def add_cookie(self, cookie_dict: dict):
        """
        添加 cookie
        
        Args:
            cookie_dict: cookie 字典
        """
        self.driver.add_cookie(cookie_dict)
        self.logger.info(f"添加 cookie: {cookie_dict.get('name', '')}")
