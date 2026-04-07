# 肖恩教务管家自动化测试项目

基于 pytest + Selenium + Allure 的 Web 自动化测试框架，用于肖恩教务管家系统的功能测试。

## 项目结构

```
XiaoEnEducationButlerTest/
├── config/                     # 配置文件目录
│   └── config.yaml            # 主配置文件（URL、浏览器、测试数据）
├── data/                       # 测试数据目录
│   ├── login_data.yaml        # 登录模块测试数据
│   └── test_data.yaml         # 通用测试数据
├── pages/                      # Page Object 模块
│   ├── base_page.py           # 基础页面类（封装 Selenium 常用操作）
│   ├── login_page.py          # 登录页面类
│   └── home_page.py           # 首页类
├── testcases/                  # 测试用例目录
│   └── test_login.py          # 登录模块测试用例
├── utils/                      # 工具模块
│   ├── logger.py              # 日志工具
│   └── data_loader.py         # 配置/数据加载器
├── reports/                    # 测试报告目录
│   ├── allure-results/        # Allure 原始数据
│   ├── allure-report/         # Allure HTML 报告
│   └── report.html            # pytest-html 报告
├── screenshots/                # 失败截图目录
├── conftest.py                 # pytest 全局配置和 fixtures
├── pytest.ini                  # pytest 配置文件
├── requirements.txt            # 项目依赖
├── run_tests.py               # 测试执行入口
├── Jenkinsfile                # Jenkins Pipeline 配置
└── README.md                   # 项目说明文档
```

## 环境要求

- Python 3.10+
- Chrome/Firefox/Edge 浏览器
- Java 17+（Allure 报告需要）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 安装 Allure 命令行工具

```bash
npm install -g allure-commandline
```

### 3. 配置测试数据

编辑 `config/config.yaml` 文件，配置测试账号：

```yaml
test_data:
  admin:
    org_code: "你的机构编码"
    phone: "你的手机号"
    password: "你的密码"
```

### 4. 运行测试

```bash
# 运行所有测试
python -m pytest testcases/ -v

# 运行冒烟测试
python -m pytest testcases/ -m smoke -v

# 运行指定模块测试
python -m pytest testcases/test_login.py -v

# 生成 Allure 报告数据
python -m pytest testcases/ --alluredir=./reports/allure-results

# 启动 Allure 在线报告
allure serve ./reports/allure-results
```

## 测试用例标记

| 标记 | 说明 |
|------|------|
| `smoke` | 冒烟测试 |
| `login` | 登录模块 |
| `p0` | 最高优先级 |
| `p1` | 高优先级 |
| `p2` | 中优先级 |
| `p3` | 低优先级 |

使用示例：
```bash
python -m pytest testcases/ -m "smoke and p0" -v
```

## Page Object 模式说明

本项目采用 Page Object 模式，将页面元素定位和操作封装在 Page 类中：

### BasePage（基础页面类）

提供通用的 Selenium 操作方法：
- `find_element()` - 查找元素
- `wait_for_visible()` - 等待元素可见
- `wait_for_clickable()` - 等待元素可点击
- `click()` - 点击元素
- `input_text()` - 输入文本
- `get_text()` - 获取文本
- `screenshot()` - 截图

### LoginPage（登录页面类）

封装登录页面的操作：
- `open_login_page()` - 打开登录页面
- `input_org_code()` - 输入机构编码
- `input_phone()` - 输入手机号码
- `input_password()` - 输入密码
- `click_login_button()` - 点击登录按钮
- `login()` - 执行完整登录流程

### HomePage（首页类）

封装首页的操作：
- `is_logged_in()` - 判断是否已登录
- `get_menu_items()` - 获取菜单项
- `click_menu_item()` - 点击菜单项
- `logout()` - 退出登录

## 编写新测试用例

### 1. 创建 Page Object

在 `pages/` 目录下创建新的 Page 类：

```python
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class StudentPage(BasePage):
    """学员管理页面"""
    
    ADD_BUTTON = (By.CSS_SELECTOR, ".add-student-btn")
    NAME_INPUT = (By.CSS_SELECTOR, "input[name='name']")
    
    def click_add_button(self):
        """点击新增按钮"""
        self.click(self.ADD_BUTTON)
```

### 2. 创建测试用例

在 `testcases/` 目录下创建测试文件：

```python
import pytest
import allure
from pages.student_page import StudentPage

@allure.feature("学员管理")
class TestStudent:
    
    @allure.title("新增学员")
    @pytest.mark.smoke
    def test_add_student(self, driver_with_screenshot, config):
        student_page = StudentPage(driver_with_screenshot, config.get("base_url"))
        student_page.click_add_button()
        # ... 更多操作
```

## 测试报告

### pytest-html 报告

```bash
python -m pytest testcases/ --html=./reports/report.html --self-contained-html
```

### Allure 报告

```bash
# 生成报告数据
python -m pytest testcases/ --alluredir=./reports/allure-results

# 启动在线报告
allure serve ./reports/allure-results

# 生成静态报告
allure generate ./reports/allure-results -o ./reports/allure-report --clean
```

## Jenkins 集成

### 项目支持

本项目完全支持 Jenkins CI/CD 集成，已包含标准的 Jenkinsfile。

### Jenkins 配置步骤

1. **安装必要插件**：
   - Git Plugin
   - Pipeline Plugin
   - Allure Report Plugin
   - HTML Publisher Plugin
   - Python Plugin

2. **创建 Pipeline 任务**：
   - 新建任务 → Pipeline
   - 源码管理：Git，配置仓库地址
   - Pipeline：选择 "Pipeline script from SCM"
   - 脚本路径：Jenkinsfile

3. **构建触发器**：
   ```
   # 每天凌晨 2 点执行
   H 2 * * *
   
   # 或代码提交时触发（配置 webhook）
   ```

4. **查看构建结果**：
   - Allure 测试报告
   - 失败截图
   - 构建日志

### Jenkinsfile 说明

项目根目录已包含 Jenkinsfile，包含以下阶段：
- 清理工作空间
- 拉取代码
- 安装依赖
- 运行自动化测试
- 生成测试报告
- 构建通知

## 配置说明

### config/config.yaml

```yaml
base_url: "https://xue.yunvip123.com"  # 测试环境地址
timeout: 10                            # 默认超时时间
implicit_wait: 10                      # 隐式等待时间
explicit_wait: 15                      # 显式等待时间

browser:
  name: "chrome"                       # 浏览器类型: chrome/firefox/edge
  headless: false                      # 是否无头模式
  window_maximize: true                # 是否最大化窗口

test_data:                             # 测试数据
  admin:
    org_code: "8888"
    phone: "8888"
    password: "123456"
```

## 常见问题

### Q: 元素定位失败？

1. 检查页面是否加载完成
2. 使用 `wait_for_visible()` 等待元素
3. 检查选择器是否正确
4. 使用调试脚本 `debug_page.py` 分析页面结构

### Q: 登录失败？

1. 确认测试账号正确
2. 检查网络连接
3. 查看日志输出
4. 检查截图文件

### Q: Allure 报告无法启动？

1. 确认已安装 Java 环境
2. 确认已安装 allure-commandline
3. 检查 PATH 环境变量

## 维护指南

### 新员工入职

1. 阅读 README.md 了解项目结构
2. 阅读 `conftest.py` 了解 fixtures 机制
3. 阅读 `pages/base_page.py` 了解基础操作
4. 参考现有测试用例编写新用例

### 代码规范

1. 所有 Page 类继承 BasePage
2. 使用显式等待代替隐式等待
3. 添加适当的日志输出
4. 测试用例添加 Allure 注解
5. 失败场景添加截图

## 更新日志

### v1.0.0 (2026-04-05)
- 初始化项目框架
- 完成登录模块测试用例
- 集成 Allure 报告
- 添加 README 文档
- 支持 Jenkins CI/CD 集成