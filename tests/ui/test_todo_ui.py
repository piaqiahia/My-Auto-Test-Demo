import allure
from playwright.sync_api import expect
from tests.ui.pages.todo_page import TodoPage

@allure.feature("TodoMVC UI 自动化")
@allure.story("核心UI测试")
def test_add_and_complete_todo(page): # 依赖注入: page 参数由 conftest.py 中的 page fixture 提供，是一个全新的浏览器页面
    todo_page = TodoPage(page) # 将 page 对象传给 TodoPage 构造函数，创建一个专门用于操作 TodoMVC 页面的对象
    todo_page.navigate() # 导航: 调用 navigate() 方法，打开目标网站并等待关键元素加载

    with allure.step("添加一个新任务"):
        todo_page.add_todo("新任务：学习PlayWright")
        assert todo_page.get_todo_count() == 1 # 数量验证: get_todo_count() == 1 确保列表中只有一个任务
        # 存在性和状态验证: assert_todo_exists(..., completed=False) 利用 POM 内部的 expect 断言，确保任务存在且未完成
        todo_page.assert_todo_exists("新任务：学习PlayWright", completed=False)

    with allure.step("标记任务为完成"):
        todo_page.toggle_todo(0) # 索引操作: toggle_todo(0) 表示操作列表中的第一个（索引为0）任务
        # 状态变更验证: 再次调用 assert_todo_exists，但这次验证 completed=True，确保勾选操作生效
        todo_page.assert_todo_exists("新任务：学习PlayWright", completed = True)

    with allure.step("截图保存状态"):
        """
        allure.attach Allure Python 适配器的核心 API 用于将任何数据作为附件附加到当前的测试用例
        body=page.screenshot() 要附加的实际内容。在这里，就是上一步获取到的 PNG 图像的二进制数据
        name="todo_completed" 附件在 Allure 报告中的显示名称
        attachment_type=allure.attachment_type.PNG 指定附件的 MIME 类型。Allure 根据这个类型来决定如何在报告中渲染附件
        """
        allure.attach(page.screenshot(), name = "todo_completed", attachment_type = allure.attachment_type.PNG)

@allure.feature("TodoMVC UI 自动化")
@allure.story("过滤功能")
def test_filter_active_items(page):
    # 测试：只显示未完成的任务
    todo_page = TodoPage(page)
    todo_page.navigate()

    # 添加两个任务
    todo_page.add_todo("已完成任务")
    todo_page.toggle_todo(0) # 已完成任务enter后点击它的复选框
    todo_page.add_todo("未完成任务")

    with allure.step("点击Active过滤"):
        todo_page.filter_active()

    # 双重验证，确保对的东西在且错的东西不在 "未完成任务"应该可见
    todo_page.assert_todo_exists("未完成任务", completed = False) # 未选中则可见
    completed_locator = page.locator("ul.todo-list li:has-text('已完成任务')")
    expect(completed_locator).not_to_be_visible()