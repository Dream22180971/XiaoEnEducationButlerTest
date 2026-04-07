"""
pytest 全局配置文件
定义共享 fixtures、钩子函数和测试环境配置
"""
import os
from datetime import datetime
from typing import Generator

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.data_loader import ConfigLoader
from utils.logger import get_logger

logger = get_logger()


def pytest_configure(config):
    """
    pytest 配置钩子，在测试开始前执行
    用于添加环境信息到 Allure 报告
    """
    allure_dir = os.path.join(os.path.dirname(__file__), "reports", "allure-results")
    os.makedirs(allure_dir, exist_ok=True)

    environment_properties = {
        "浏览器": ConfigLoader.get("browser.name", "chrome"),
        "基础URL": ConfigLoader.get("base_url", ""),
        "测试环境": "测试环境",
        "Python版本": "3.10+",
        "测试框架": "pytest + Selenium + Allure",
    }

    env_file = os.path.join(allure_dir, "environment.properties")
    with open(env_file, "w", encoding="utf-8") as f:
        for key, value in environment_properties.items():
            f.write(f"{key}={value}\n")

    logger.info("pytest 配置完成，Allure 环境信息已写入")


@pytest.fixture(scope="session")
def config() -> dict:
    """
    加载配置文件的 fixture
    
    Returns:
        配置字典
    """
    logger.info("加载配置文件")
    return ConfigLoader.load_config()


@pytest.fixture(scope="session")
def driver(config: dict) -> Generator:
    """
    WebDriver fixture，整个测试会话共享一个浏览器实例
    
    Args:
        config: 配置字典 fixture
        
    Yields:
        WebDriver 实例
    """
    browser_name = config.get("browser", {}).get("name", "chrome").lower()
    headless = config.get("browser", {}).get("headless", False)
    maximize = config.get("browser", {}).get("window_maximize", True)
    window_size = config.get("browser", {}).get("window_size", {})
    implicit_wait = config.get("implicit_wait", 10)

    logger.info(f"初始化浏览器: {browser_name}, 无头模式: {headless}")

    driver = None

    try:
        if browser_name == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--window-size=1920,1080")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

        elif browser_name == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")

            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)

        elif browser_name == "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)

        else:
            raise ValueError(f"不支持的浏览器类型: {browser_name}")

        driver.implicitly_wait(implicit_wait)

        if maximize:
            driver.maximize_window()
        elif window_size:
            width = window_size.get("width", 1920)
            height = window_size.get("height", 1080)
            driver.set_window_size(width, height)

        logger.info(f"浏览器初始化成功: {browser_name}")

        yield driver

    except Exception as e:
        logger.error(f"浏览器初始化失败: {str(e)}")
        raise

    finally:
        if driver:
            logger.info("关闭浏览器")
            driver.quit()


@pytest.fixture(scope="function")
def driver_with_screenshot(driver, request):
    """
    带自动截图功能的 driver fixture
    测试失败时自动截图并附加到 Allure 报告
    
    Args:
        driver: WebDriver fixture
        request: pytest request 对象
        
    Yields:
        WebDriver 实例
    """
    yield driver

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name
        screenshot_filename = f"{test_name}_{timestamp}.png"
        screenshot_path = os.path.join(screenshot_dir, screenshot_filename)

        try:
            driver.save_screenshot(screenshot_path)
            logger.info(f"测试失败截图已保存: {screenshot_path}")

            with open(screenshot_path, "rb") as f:
                allure.attach(
                    f.read(),
                    name=f"失败截图 - {test_name}",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            logger.error(f"截图失败: {str(e)}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest 钩子，用于获取测试结果
    使 driver_with_screenshot fixture 能够检测测试失败
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="function")
def login_page_url(config: dict) -> str:
    """
    获取登录页面 URL
    
    Args:
        config: 配置字典 fixture
        
    Returns:
        登录页面完整 URL
    """
    base_url = config.get("base_url", "")
    return f"{base_url}/login"


@pytest.fixture(scope="session")
def test_data(config: dict) -> dict:
    """
    获取测试数据
    
    Args:
        config: 配置字典 fixture
        
    Returns:
        测试数据字典
    """
    return config.get("test_data", {})


@pytest.fixture(scope="function")
def admin_credentials(test_data: dict) -> dict:
    """
    获取管理员账号凭据
    
    Args:
        test_data: 测试数据 fixture
        
    Returns:
        管理员账号信息字典
    """
    return test_data.get("admin", {})


@pytest.fixture(scope="function")
def teacher_credentials(test_data: dict) -> dict:
    """
    获取教师账号凭据
    
    Args:
        test_data: 测试数据 fixture
        
    Returns:
        教师账号信息字典
    """
    return test_data.get("teacher", {})


@pytest.fixture(scope="function")
def parent_credentials(test_data: dict) -> dict:
    """
    获取家长账号凭据
    
    Args:
        test_data: 测试数据 fixture
        
    Returns:
        家长账号信息字典
    """
    return test_data.get("parent", {})


def pytest_collection_modifyitems(config, items):
    """
    pytest 钩子，用于修改测试用例收集结果
    为没有标记的测试用例添加默认标记
    """
    for item in items:
        if not list(item.iter_markers()):
            item.add_marker(pytest.mark.p1)
