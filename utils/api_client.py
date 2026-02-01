import requests
from utils.logger import get_logger

logger = get_logger(__name__) # 创建模块级日志记录器 将当前文件名传给get_logger 方便显示哪里出了问题

class ApiClient:
    def __init__(self, base_url = "https://httpbin.org/"): # base_url: API 的根地址
        self.base_url = base_url
        self.session = requests.Session() # 创建会话实现TCP连接复用
        self.session.headers.update({
            "Content-Type" : "application/json",
            # "Authorization": "Bearer token_if_needed"
        })

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"发送请求：{method}{url}|paramas:{kwargs}")

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            logger.info(f"响应成功：{response.status_code}|body:{response.text[:200]}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败：{e}")
            raise
    # 公共接口方法
    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint, json_data = None, **kwargs):
        return self._request("POST", endpoint, json = json_data, **kwargs)

    def put(self, endpoint, json_data=None, **kwargs):
        return self._request("PUT", endpoint, json=json_data, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)