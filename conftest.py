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

