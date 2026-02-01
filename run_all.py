import os
import platform
import shutil
import subprocess
import sys

# --- 配置区 ---
# 定义各个工具的命令和参数，方便未来修改

# 运行 tests/ 目录下所有测试 "tests/"：匹配 pytest.ini 中的 testpaths = tests/api, tests/ui
# "--alluredir=..."：指定 Allure 原始结果（JSON 文件）存储路径 "-v"：显示详细用例名称（verbose 模式）
PYTEST_CMD = ["pytest", "tests/", "--alluredir=reports/allure_results", "-v"]

# 将原始结果转换为可视化 HTML 报告 --clean：如果输出目录已存在，先清空再写入（避免 JMeter 式的“目录非空”错误） 否则多次运行会失败
ALLURE_BIN = "allure.bat" if platform.system() == "Windows" else "allure"

ALLURE_GENERATE_CMD = [ALLURE_BIN,
                       "generate", "reports/allure_results",
                       "-o", "reports/allure_report",
                       "--clean"]

# 自动选择正确的 JMeter 启动命令 Windows 上 jmeter 是一个 .bat 脚本，Python 的 subprocess 不会自动补全扩展名 Linux jmeter即可
JMETER_BIN = "jmeter.bat" if platform.system() == "Windows" else "jmeter"

# 以非 GUI 模式运行 JMeter 脚本
# result.jtl：JMeter 默认结果格式（XML），比 CSV 更通用
JMETER_RUN_CMD = [
    JMETER_BIN,
    "-n",
    "-t", "jmeter_script/View_Results_Tree1.jmx", # 指定要运行的 .jmx 脚本路径
    "-l", "jmeter_script/result.jtl" # 指定结果日志输出文件（.jtl 格式）
]

JMETER_REPORT_CMD = [
    JMETER_BIN,
    "-g", "jmeter_script/result.jtl", # 输入上一步生成的 .jtl 日志文件
    "-o", "reports/jmeter_report" # 输出HTML 报告目录（必须不存在或为空！）
]

def run_command(command, cwd = ".", allow_failure=False):
    """
    执行外部命令。
    - 如果命令未找到（FileNotFoundError），返回 False 并终止。
    - 如果命令执行失败（returncode != 0）：
        - allow_failure=True：仅打印警告，返回 True
        - allow_failure=False：视为错误，返回 False
    """
    print(f"\n{'=' * 20}正在执行命令：{' '.join(command)}{'=' * 20}")
    try:
        result = subprocess.run( # subprocess.run() 是 Python 中 执行外部命令、启动子进程 的核心函数
            command, # arg,必须为list
            check = False, # 选择手动处理 returncode
            capture_output = True, # 捕获 stdout/stderr
            text = True,  # 返回字符串而非 bytes
            cwd = cwd, # 设置工作目录
            encoding = 'utf-8', # 避免 Windows GBK 解码错误
            errors = 'replace' # 非法字符替换为' '，防崩溃
        )

        print("---命令标准输出（stdout）---")
        print(result.stdout)
        if result.stderr.strip(): # 即使成功也可能有 stderr（如警告），所以单独判断 strip()
            print("命令标准错误（stderr）---")
            print(result.stderr)

        if result.returncode == 0:
            print(f"---命令执行成功，返回码：{result.returncode}---")
            return True
        else:
            if allow_failure:
                print(f"[警告]命令'{' '.join(command)}'执行完成但有失败（返回码：{result.returncode}），继续执行后续代码")
                return True
            else:
                print(f"[错误]命令'{' '.join(command)}'执行失败，返回码：{result.returncode}")

    except FileNotFoundError:
        print(f"[错误]命令'{command[0]}'未找到，请确保配置正确并已安装在PATH中")
        return False
    except Exception as e:
        print(f"[异常]执行命令是发生错误：{e}")
        return False

# 执行主逻辑
def main():
    print("=" * 60)
    print("开始执行一体化自动化测试流程（宽松模式：测试失败也继续）")
    print("=" * 60)

    base_path = os.path.dirname(os.path.abspath(__file__))
    print(f"项目基准目录：{base_path}")

    # 执行pytest 允许测试用例失败
    pytest_success = run_command(PYTEST_CMD, cwd = base_path, allow_failure = True)

    # 生成allure报告（包含失败用例）
    allure_success = run_command(ALLURE_GENERATE_CMD, cwd = base_path, allow_failure = False)
    if allure_success:
        print("\n Allure报告已生成，请查看：reports/allure_results/index.html")
    else:
        print("\n Allure报告生成失败（可能无测试结果），跳过")

    # 清理 JMeter 报告目录（JMeter -o 要求目录为空）
    jmeter_report_dir = os.path.join(base_path, "reports", "jmeter_report")
    if os.path.exists(jmeter_report_dir):
        shutil.rmtree(jmeter_report_dir)

    jmeter_run_success = run_command(JMETER_RUN_CMD, cwd = base_path, allow_failure = False)
    jmeter_report_success = True # JMeter 脚本错误（如 .jmx 语法错误）会终止流程
    if jmeter_run_success:
        jmeter_report_success = run_command(JMETER_REPORT_CMD, cwd = base_path, allow_failure = False)
        if jmeter_report_success:
            print("\n Jmeter HTML报告已生成...")
    else:
        print("\n JMeter 压测未执行，跳过报告生成...")

    print("\n" + "=" * 60)
    if pytest_success and jmeter_report_success and jmeter_run_success:
        print("所有测试及报告完成")
        sys.exit(0)
    else:
        print("部分任务失败或跳过，但流程已完整执行")
        sys.exit(0) # 宽松模式：始终返回 0

if __name__ == "__main__":
    main()

# import os
# import subprocess # 用于启动子进程
# import sys # 用于控制程序退出 常用于 CI/CD 中表示构建失败
#
# def run_api_test():
#     print("=" * 50)
#     print("开始运行 API 自动化测试 (Pytest + Allure)...")
#     print("=" * 50)
#     try:
#         result = subprocess.run( # 关键调用：启动 pytest
#             ["pytest", "-v"], # 以列表形式传命令，避免 shell 注入风险
#             capture_output = True, # 捕获 stdout 和 stderr
#             text = True, # 返回字符串而非字节
#             encoding='utf-8', # 显式指定编码
#             errors='replace', # 遇到非法字符时替换（而不是抛异常） 非法字符替换为 ，避免崩溃
#             check = False # 不抛异常，手动判断 即使 pytest 返回非 0（有失败用例），也不抛异常
#         )
#         print(result.stdout) # 打印 pytest 的标准输出（包括 PASSED/FAILED 等信息）便于调试
#         if result.stderr: # 如果有标准错误输出（如警告、异常堆栈），也打印出来
#             print("stderr", result.stderr)
#         if "failed" in result.stdout or result.returncode != 0: # 检查是否有失败（通过文本或退出码）
#             print("注意：部分测试用例失败，但将继续执行后续任务。")
#             # 无论成功失败，都返回 True（表示“已执行”） 避免有用例未通过导致程序中断
#         return True
#     except Exception as e:
#         print(f"执行pytest出错：{e}")
#         return False
#
# def run_jmeter():
#     print("\n" + "=" * 50)
#     print("开始运行 JMeter 性能测试...")
#     print("=" * 50)
#
#     jmx_path = "jmeter_script/View_Results_Tree.jmx" # jmx导入路径
#     report_dir = "reports/jmeter_report" # JMeter HTML 报告输出目录
#
#     # 确保报告目录存在（JMeter 要求目录为空或不存在）
#     if os.path.exists(report_dir):
#         import shutil
#         shutil.rmtree(report_dir) # JMeter 要求 -o 目录必须不存在或为空，所以先删除旧报告
#
#     cmd = [
#         "jmeter.bat",
#         "-n", # 非 GUI 模式
#         "-t", jmx_path, # 指定 .jmx 脚本
#         "-l", "jmeter_script/result.jtl",  # 结果日志 保存结果到 .jtl（XML/CSV）
#         "-e", # 生成 Dashboard
#         "-o", report_dir
#     ]
#
#     try:
#         result = subprocess.run(
#             cmd,
#             capture_output = True,
#             text = True,
#             encoding='utf-8',  # 显式指定编码
#             errors='replace',  # 遇到非法字符时替换（而不是抛异常）
#             check = False
#         )
#         print(result.stdout)
#         if result.stderr:
#             print("STDERR", result.stderr)
#         if result.returncode != 0:
#             print("Jmeter执行失败！")
#             return False
#         else:
#             print(f"Jmeter报告已生成：{os.path.abspath(report_dir)}/index.html")
#             return True
#     except FileNotFoundError:
#         print("错误！Jmeter未加入PATH或未安装，请先安装Apache Jmeter并配置环境变量")
#         return False
#     except Exception as e:
#         print(f"执行Jmeter时出错：{e}")
#         return False
#
# if __name__ == "__main__":
#     print("自动化测试一键执行脚本启动中...\n")
#
#     api_success = run_api_test()
#
#     if api_success:
#         jmeter_success = run_jmeter()
#     else:
#         print("\n 由于 API 测试失败，跳过 JMeter 性能测试 ")
#         jmeter_success = True #  或设为 False，根据策略
#
#     print("\n" + "=" * 50)
#     if api_success and jmeter_success:
#         print("所有测试执行成功！")
#     else:
#         print("有测试环节失败，请检查日志。")
#         sys.exit(1) # 让 CI 知道构建失败