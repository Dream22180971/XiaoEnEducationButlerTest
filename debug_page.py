"""
页面元素调试脚本
用于获取页面实际元素结构，帮助定位正确的元素选择器
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.data_loader import ConfigLoader

config = ConfigLoader.load_config()
base_url = config.get("base_url", "")

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

try:
    print(f"\n打开页面: {base_url}/#/auth/login")
    driver.get(f"{base_url}/#/auth/login")
    time.sleep(3)

    print("\n=== 页面标题 ===")
    print(driver.title)

    print("\n=== 当前 URL ===")
    print(driver.current_url)

    print("\n=== 查找输入框 ===")
    inputs = driver.find_elements("css selector", "input")
    for i, inp in enumerate(inputs):
        try:
            print(f"  Input {i+1}:")
            print(f"    type: {inp.get_attribute('type')}")
            print(f"    placeholder: {inp.get_attribute('placeholder')}")
        except:
            pass

    print("\n=== 查找按钮 ===")
    buttons = driver.find_elements("css selector", "button")
    for i, btn in enumerate(buttons):
        try:
            print(f"  Button {i+1}:")
            print(f"    text: {btn.text}")
            print(f"    class: {btn.get_attribute('class')}")
        except:
            pass

    print("\n=== 尝试登录 ===")
    org_code = config.get("test_data", {}).get("admin", {}).get("org_code", "")
    phone = config.get("test_data", {}).get("admin", {}).get("phone", "")
    password = config.get("test_data", {}).get("admin", {}).get("password", "")
    
    org_input = driver.find_element("css selector", "input[placeholder*='机构编码']")
    org_input.clear()
    org_input.send_keys(org_code)
    print(f"输入机构编码: {org_code}")

    phone_input = driver.find_element("css selector", "input[placeholder*='手机']")
    phone_input.clear()
    phone_input.send_keys(phone)
    print(f"输入手机号码: {phone}")

    password_input = driver.find_element("css selector", "input[placeholder*='密码']")
    password_input.clear()
    password_input.send_keys(password)
    print(f"输入密码: {password}")

    login_btn = driver.find_element("css selector", "button.el-button--primary")
    login_btn.click()
    print("点击登录按钮")

    time.sleep(5)

    print("\n=== 登录后页面 ===")
    print(f"URL: {driver.current_url}")
    print(f"Title: {driver.title}")

    print("\n=== 登录后所有重要元素 ===")
    
    print("\n--- 带有 'user' 类名的元素 ---")
    user_elements = driver.find_elements("css selector", "[class*='user']")
    for i, elem in enumerate(user_elements[:10]):
        try:
            print(f"  {i+1}. class: {elem.get_attribute('class')}, text: {elem.text[:30] if elem.text else ''}")
        except:
            pass

    print("\n--- 带有 'avatar' 类名的元素 ---")
    avatar_elements = driver.find_elements("css selector", "[class*='avatar']")
    for i, elem in enumerate(avatar_elements[:10]):
        try:
            print(f"  {i+1}. class: {elem.get_attribute('class')}")
        except:
            pass

    print("\n--- 带有 'menu' 类名的元素 ---")
    menu_elements = driver.find_elements("css selector", "[class*='menu']")
    for i, elem in enumerate(menu_elements[:10]):
        try:
            print(f"  {i+1}. class: {elem.get_attribute('class')}")
        except:
            pass

    print("\n--- 带有 'sidebar' 类名的元素 ---")
    sidebar_elements = driver.find_elements("css selector", "[class*='sidebar']")
    for i, elem in enumerate(sidebar_elements[:10]):
        try:
            print(f"  {i+1}. class: {elem.get_attribute('class')}")
        except:
            pass

    print("\n--- 带有 'nav' 类名的元素 ---")
    nav_elements = driver.find_elements("css selector", "[class*='nav']")
    for i, elem in enumerate(nav_elements[:10]):
        try:
            print(f"  {i+1}. class: {elem.get_attribute('class')}")
        except:
            pass

    print("\n--- 所有 header 元素 ---")
    header_elements = driver.find_elements("css selector", "header, .header")
    for i, elem in enumerate(header_elements[:5]):
        try:
            print(f"  {i+1}. class: {elem.get_attribute('class')}")
        except:
            pass

    print("\n--- 页面主体结构 ---")
    main_divs = driver.find_elements("css selector", "div[class]")[:20]
    for i, div in enumerate(main_divs):
        try:
            cls = div.get_attribute("class")
            if len(cls) < 100:
                print(f"  {i+1}. {cls}")
        except:
            pass

    driver.save_screenshot("debug_after_login.png")
    print("\n截图已保存: debug_after_login.png")

    input("\n按回车键关闭浏览器...")

finally:
    driver.quit()
