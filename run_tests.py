"""
运行测试脚本
提供多种测试执行方式的快捷命令
"""
import os
import subprocess
import sys


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("运行所有测试用例...")
    print("=" * 50)
    subprocess.run([
        sys.executable, "-m", "pytest",
        "-v", "-s",
        "--alluredir=./reports/allure-results",
        "--clean-alluredir"
    ])


def run_smoke_tests():
    """运行冒烟测试"""
    print("=" * 50)
    print("运行冒烟测试...")
    print("=" * 50)
    subprocess.run([
        sys.executable, "-m", "pytest",
        "-v", "-s",
        "-m", "smoke",
        "--alluredir=./reports/allure-results",
        "--clean-alluredir"
    ])


def run_p0_tests():
    """运行 P0 级别测试"""
    print("=" * 50)
    print("运行 P0 级别测试...")
    print("=" * 50)
    subprocess.run([
        sys.executable, "-m", "pytest",
        "-v", "-s",
        "-m", "p0",
        "--alluredir=./reports/allure-results",
        "--clean-alluredir"
    ])


def run_login_tests():
    """运行登录模块测试"""
    print("=" * 50)
    print("运行登录模块测试...")
    print("=" * 50)
    subprocess.run([
        sys.executable, "-m", "pytest",
        "-v", "-s",
        "-m", "login",
        "--alluredir=./reports/allure-results",
        "--clean-alluredir"
    ])


def run_parallel_tests():
    """并行运行测试（4个进程）"""
    print("=" * 50)
    print("并行运行测试（4个进程）...")
    print("=" * 50)
    subprocess.run([
        sys.executable, "-m", "pytest",
        "-v", "-s",
        "-n", "4",
        "--alluredir=./reports/allure-results",
        "--clean-alluredir"
    ])


def generate_allure_report():
    """生成 Allure 报告"""
    print("=" * 50)
    print("生成 Allure 报告...")
    print("=" * 50)
    subprocess.run([
        "allure", "generate",
        "./reports/allure-results",
        "-o", "./reports/allure-report",
        "--clean"
    ])
    print("\n报告生成完成，执行以下命令查看报告:")
    print("allure open ./reports/allure-report")


def open_allure_report():
    """打开 Allure 报告"""
    print("=" * 50)
    print("打开 Allure 报告...")
    print("=" * 50)
    subprocess.run(["allure", "open", "./reports/allure-report"])


def install_dependencies():
    """安装项目依赖"""
    print("=" * 50)
    print("安装项目依赖...")
    print("=" * 50)
    subprocess.run([
        sys.executable, "-m", "pip",
        "install", "-r", "requirements.txt"
    ])


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("小禾帮教务管理系统 - 自动化测试运行器")
    print("=" * 50)
    print("\n可用命令:")
    print("  1. run_all_tests()      - 运行所有测试")
    print("  2. run_smoke_tests()    - 运行冒烟测试")
    print("  3. run_p0_tests()       - 运行 P0 级别测试")
    print("  4. run_login_tests()    - 运行登录模块测试")
    print("  5. run_parallel_tests() - 并行运行测试")
    print("  6. generate_report()    - 生成 Allure 报告")
    print("  7. open_report()        - 打开 Allure 报告")
    print("  8. install_deps()       - 安装项目依赖")
    print("\n使用示例:")
    print("  python run_tests.py")
    print("  然后在交互模式下输入: run_all_tests()")
    print("=" * 50 + "\n")
