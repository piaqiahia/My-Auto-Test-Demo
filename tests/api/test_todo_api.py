import allure
from utils.api_client import ApiClient

@allure.feature("Todo API 模拟测试(HttpBin)") # 定义该用例所属模块 所有带有相同 feature 的用例会被归为一组
@allure.story("POST 创建资源") # 在 feature 下进一步细分，代表一个具体的用户故事或业务场景
def test_create_todo_api(api_client: ApiClient, test_data):
    """
    模拟向后端发送创建 Todo 的请求
    使用 HttpBin 的 /post 接口，它会返回我们发送的 JSON 数据
    流程：准备: 从 YAML 文件加载测试数据 payload
        执行: 通过 api_client 向 httpbin.org/post 发送一个 POST 请求
        验证:检查 HTTP 状态码是否为 200。检查响应体中的 json 字段是否包含了我们发送的 title 和 completed 字段
        记录: 将完整的 API 响应作为 JSON 附件保存到 Allure 报告中
    """
    # 从注入的 test_data 字典中提取名为 "new_task_payload" 的子字典作为本次请求的 JSON 负载。 数据驱动测试
    payload = test_data["new_task_payload"]
    """
    allure.step: 将一段代码逻辑标记为一个独立的、有语义的步骤
    在 Allure 报告中，这个测试用例会被分解成多个清晰的步骤
    如果测试失败，可以立刻定位到是哪个具体步骤出了问题,让测试代码的可读性更强
    """
    with allure.step("发送POST请求创建Todo"):
        response = api_client.post("/post", json_data = payload)

    with allure.step("验证状态码"):
        assert response.status_code == 200

    with allure.step("验证响应体中的数据"):
        resp_json = response.json()
        assert resp_json["json"]["title"] == payload["title"]
        assert resp_json["json"]["completed"] == payload["completed"]

    """
    添加附件 (Attachments) 将任何信息（文本、图片、视频、文件等）作为附件附加到当前的测试用例或步骤中
    response.text: 要附加的内容，这里是完整的 API 响应文本
    name="api_response": 附件在报告中的显示名称
    attachment_type=allure.attachment_type.JSON: 指定附件类型为 JSON。Allure 会对其进行语法高亮
    """
    allure.attach(response.text, name = "api_response", attachment_type = allure.attachment_type.JSON)