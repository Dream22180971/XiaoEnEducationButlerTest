"""
登录模块测试用例
包含登录功能的正向测试、逆向测试和边界测试
"""
import allure
import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage


@allure.feature("登录模块")
@allure.story("机构用户登录")
class TestLogin:
    """
    登录功能测试类
    测试各种登录场景，包括成功登录、失败登录、边界条件等
    """

    @allure.title("登录页面元素验证")
    @allure.description("验证登录页面的关键元素是否正确显示")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.p1
    def test_login_page_elements(self, driver, config):
        """
        测试登录页面元素是否正确显示
        
        Steps:
            1. 打开登录页面
            2. 验证机构编码输入框存在
            3. 验证手机号码输入框存在
            4. 验证密码输入框存在
            5. 验证登录按钮存在
        """
        login_page = LoginPage(driver, config.get("base_url", ""))
        login_page.open_login_page()

        assert login_page.verify_login_page_elements(), "登录页面元素验证失败"

    @allure.title("管理员账号成功登录")
    @allure.description("使用正确的管理员账号密码进行登录")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.p0
    def test_admin_login_success(self, driver_with_screenshot, config, admin_credentials):
        """
        测试管理员账号成功登录
        
        Steps:
            1. 打开登录页面
            2. 输入机构编码
            3. 输入手机号码
            4. 输入密码
            5. 点击登录按钮
            6. 验证登录成功
        """
        driver = driver_with_screenshot
        login_page = LoginPage(driver, config.get("base_url", ""))
        home_page = HomePage(driver, config.get("base_url", ""))

        with allure.step("步骤1: 打开登录页面"):
            login_page.open_login_page()

        with allure.step("步骤2: 输入机构编码"):
            login_page.input_org_code(admin_credentials.get("org_code", ""))

        with allure.step("步骤3: 输入手机号码"):
            login_page.input_phone(admin_credentials.get("phone", ""))

        with allure.step("步骤4: 输入密码"):
            login_page.input_password(admin_credentials.get("password", ""))

        with allure.step("步骤5: 点击登录按钮"):
            login_page.click_login_button()

        with allure.step("步骤6: 验证登录成功"):
            login_page.wait_for_page_load()
            assert home_page.is_logged_in(), "管理员登录失败"

    @allure.title("教师账号成功登录")
    @allure.description("使用正确的教师账号密码进行登录")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login
    @pytest.mark.p1
    def test_teacher_login_success(self, driver_with_screenshot, config, teacher_credentials):
        """
        测试教师账号成功登录
        """
        driver = driver_with_screenshot
        login_page = LoginPage(driver, config.get("base_url", ""))
        home_page = HomePage(driver, config.get("base_url", ""))

        login_page.open_login_page()
        login_page.login(
            teacher_credentials.get("org_code", ""),
            teacher_credentials.get("phone", ""),
            teacher_credentials.get("password", "")
        )

        login_page.wait_for_page_load()
        assert home_page.is_logged_in(), "教师登录失败"

    @allure.title("空机构编码登录失败")
    @allure.description("不输入机构编码，验证登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.p1
    def test_login_with_empty_org_code(self, driver_with_screenshot, config):
        """
        测试空机构编码登录
        """
        driver = driver_with_screenshot
        login_page = LoginPage(driver, config.get("base_url", ""))

        login_page.open_login_page()
        login_page.input_phone("13800138000")
        login_page.input_password("123456")
        login_page.click_login_button()

        assert not login_page.is_login_successful(), "空机构编码登录应该失败"

    @allure.title("空手机号码登录失败")
    @allure.description("不输入手机号码，验证登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.p1
    def test_login_with_empty_phone(self, driver_with_screenshot, config):
        """
        测试空手机号码登录
        """
        driver = driver_with_screenshot
        login_page = LoginPage(driver, config.get("base_url", ""))

        login_page.open_login_page()
        login_page.input_org_code("8888")
        login_page.input_password("123456")
        login_page.click_login_button()

        assert not login_page.is_login_successful(), "空手机号码登录应该失败"

    @allure.title("空密码登录失败")
    @allure.description("输入机构编码和手机号码，不输入密码，验证登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.p1
    def test_login_with_empty_password(self, driver_with_screenshot, config):
        """
        测试空密码登录
        """
        driver = driver_with_screenshot
        login_page = LoginPage(driver, config.get("base_url", ""))

        login_page.open_login_page()
        login_page.input_org_code("8888")
        login_page.input_phone("13800138000")
        login_page.click_login_button()

        assert not login_page.is_login_successful(), "空密码登录应该失败"

    @allure.title("错误密码登录失败")
    @allure.description("使用正确的机构编码和手机号码但错误的密码登录")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login
    @pytest.mark.p0
    def test_login_with_wrong_password(self, driver_with_screenshot, config):
        """
        测试错误密码登录
        """
        driver = driver_with_screenshot
        login_page = LoginPage(driver, config.get("base_url", ""))

        login_page.open_login_page()
        login_page.login("8888", "13800138000", "wrongpassword123")

        assert not login_page.is_login_successful(), "错误密码登录应该失败"

    @allure.title("不存在的手机号登录失败")
    @allure.description("使用不存在的手机号码登录")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login
    @pytest.mark.p0
    def test_login_with_nonexistent_phone(self, driver_with_screenshot, config):
        """
        测试不存在的手机号码登录
        """
        driver = driver_with_screenshot
        login_page = LoginPage(driver, config.get("base_url", ""))

        login_page.open_login_page()
        login_page.login("8888", "99999999999", "123456")

        assert not login_page.is_login_successful(), "不存在的手机号登录应该失败"

    @allure.title("错误机构编码登录失败")
    @allure.description("使用错误的机构编码登录")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login
    @pytest.mark.p0
    def test_login_with_wrong_org_code(self, driver_with_screenshot, config):
        """
        测试错误机构编码登录
        """
        driver = driver_with_screenshot
        login_page = LoginPage(driver, config.get("base_url", ""))

        login_page.open_login_page()
        login_page.login("99999", "13800138000", "123456")

        assert not login_page.is_login_successful(), "错误机构编码登录应该失败"

    @allure.title("密码输入框类型验证")
    @allure.description("验证密码输入框是否为密码类型")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.login
    @pytest.mark.p2
    def test_password_field_type(self, driver_with_screenshot, config):
        """
        测试密码输入框类型
        """
        driver = driver_with_screenshot
        login_page = LoginPage(driver, config.get("base_url", ""))

        login_page.open_login_page()

        password_type = login_page.get_attribute(login_page.PASSWORD_INPUT, "type")
        assert password_type == "password", "密码输入框类型应为 password"


@allure.feature("登录模块")
@allure.story("登录安全性测试")
class TestLoginSecurity:
    """
    登录安全性测试类
    测试 SQL 注入、XSS 等安全场景
    """

    @allure.title("SQL注入测试")
    @allure.description("在手机号码中输入 SQL 注入字符串")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login
    @pytest.mark.p0
    @pytest.mark.parametrize("injection_string", [
        "admin' OR '1'='1",
        "admin'--",
        "' OR '1'='1' --",
    ])
    def test_sql_injection(self, driver_with_screenshot, config, injection_string):
        """
        测试 SQL 注入攻击
        """
        driver = driver_with_screenshot
        login_page = LoginPage(driver, config.get("base_url", ""))

        login_page.open_login_page()
        login_page.login("8888", injection_string, "123456")

        assert not login_page.is_login_successful(), \
            f"SQL 注入攻击应该被阻止: {injection_string}"


@allure.feature("登录模块")
@allure.story("登录性能测试")
class TestLoginPerformance:
    """
    登录性能测试类
    测试登录响应时间等性能指标
    """

    @allure.title("登录响应时间测试")
    @allure.description("验证登录操作的响应时间是否符合要求")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.p2
    def test_login_response_time(self, driver_with_screenshot, config, admin_credentials):
        """
        测试登录响应时间
        """
        import time

        driver = driver_with_screenshot
        login_page = LoginPage(driver, config.get("base_url", ""))
        home_page = HomePage(driver, config.get("base_url", ""))

        login_page.open_login_page()

        start_time = time.time()
        login_page.login(
            admin_credentials.get("org_code", ""),
            admin_credentials.get("phone", ""),
            admin_credentials.get("password", "")
        )
        login_page.wait_for_page_load()
        end_time = time.time()

        response_time = end_time - start_time
        allure.attach(
            f"登录响应时间: {response_time:.2f} 秒",
            name="响应时间",
            attachment_type=allure.attachment_type.TEXT
        )

        assert response_time < 5, f"登录响应时间 {response_time:.2f}s 超过 5 秒"
        assert home_page.is_logged_in(), "登录失败"
