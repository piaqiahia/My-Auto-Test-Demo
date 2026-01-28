import allure
import pytest
import yaml
from utils.api_client import ApiClient
from utils.logger import get_logger

logger = get_logger(__name__)

def load_test_data():
    with open("data/todo_data.yaml", "r", encoding = "utf-8") as f:
        return yaml.safe_load(f) # safe_load 只允许加载基本的 Python 数据类型（如字典、列表、字符串、数字等）

@pytest.fixture(scope="session")
def test_data():
    return load_test_data()

@pytest.fixture(scope="session")
def api_client():
    logger.info("=== 初始化 ApiClient (HttpBin) ===")
    client = ApiClient()
    yield client
    logger.info("=== 销毁 ApiClient ===")

@pytest.fixture # 不指定则默认function 调用时如果形参有page pytest将自动调入
def page():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        page = browser.new_page()
        yield page
        browser.close()


# ===== 失败自动截图钩子 =====
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    当测试用例失败时，自动附加页面截图到 Allure 报告。
    """
    outcome = yield
    rep = outcome.get_result()

    # 我们只关心测试用例的实际执行阶段（call），并且是失败的情况
    if rep.when == "call" and rep.failed:
        # 尝试从 fixture 中获取 page 对象
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            try:
                # 捕获失败瞬间的屏幕截图
                screenshot = page.screenshot()
                allure.attach(
                    screenshot,
                    name="❌_FAILURE_SCREENSHOT",
                    attachment_type=allure.attachment_type.PNG
                )
                logger.error("已将失败截图附加到 Allure 报告。")
            except Exception as e:
                logger.error(f"捕获失败截图时出错: {e}")