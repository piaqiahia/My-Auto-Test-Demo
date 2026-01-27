from playwright.sync_api import Page, expect

"""
封装: 隐藏了底层的 Playwright API 调用细节和复杂的 CSS 选择器。
抽象: 向测试用例提供的是高层次的、业务导向的方法（如 add_todo, toggle_todo），而不是低层次的 click 或 fill。
稳定性: 通过在每个操作后加入智能等待 (wait_for_selector)，确保了测试对页面加载速度不敏感。
可维护性: 元素定位器集中管理，一处修改，处处生效。
可读性: 测试用例代码变得像自然语言一样流畅。
"""

class TodoPage: # 元素定位符集合
    # 将页面上所有关键元素的定位器（CSS Selector）作为类的私有常量（以 _ 开头）集中定义在类的顶部
    _new_todo_input = "input.new-todo"
    _todo_list = "ul.todo-list li"
    _toggle_all = "input#toggle-all"
    _filter_active = "a[href='#/active']"
    _filter_completed = "a[href='#/completed']"
    _clear_completed = "button.clear-completed"

    def __init__(self, page: Page): # 依赖注入: TodoPage 的构造函数接收一个 playwright.sync_api.Page 对象
        self.page = page

    def navigate(self): # 导航到 TodoMVC 页面，并等待关键元素加载完成 等待元素加载（最多10秒）
        self.page.goto("https://demo.playwright.dev/todomvc")
        self.page.wait_for_selector(self._new_todo_input, state = "visible", timeout = 10000)

    def filter_active(self):
        self.page.click(self._filter_active)
    
    def add_todo(self, task_name: str):
        self.page.fill(self._new_todo_input, task_name)
        self.page.press(self._new_todo_input, "Enter")
        # :has-text()  伪类选择器(选择器引擎) 匹配所有内部文本内容包含 task_name 字符串的元素
        self.page.wait_for_selector(f"{self._todo_list}:has-text('{task_name}'):visible", timeout = 10000)

    def get_todo_count(self) -> int:
        # 返回当前可见的任务数量 :visible 过滤器确保只计算当前视图下可见的任务 在“Active”过滤器下，已完成的任务是不可见的，不会被计入
        return self.page.locator(f"{self._todo_list}:visible").count()

    def toggle_todo(self, index: int):
        """
        self.page.locator(self._todo_list)在整个页面 (self.page) 上创建一个 Locator 对象，用于匹配所有符合 self._todo_list 选择器的元素
        .nth(index):  从上一步得到的元素列表中，选取第 index 个元素 Playwright 会自动等待这个特定的第index个元素出现在页面上，并且处于可操作状态
        .locator("input[type='checkbox']"):.locator() 方法如果被调用在一个已有的 Locator 上，它的搜索范围就被严格限制在这个父元素内部
        .click():点击之前找到的那个元素（这里是复选框）
        """
        self.page.locator(self._todo_list).nth(index).locator("input[type='checkbox']").click()

    def delete_todo(self, index: int):
        # 分别模拟勾选/取消勾选任务和删除任务 locator().nth().locator():精确定位嵌套元素
        # todo_item.locator("button.destroy")：在 todo_item 这个特定的 <li> 元素内部，查找一个标签为button且class包含destroy的元素
        todo_item = self.page.locator(self._todo_list).nth(index)
        todo_item.hover() # 先调用 hover()，因为 TodoMVC 的删除按钮只有在鼠标悬停时才会出现
        todo_item.locator("button.destroy").click()

    def assert_todo_exists(self, task_name: str, completed: bool = None):
        locator = self.page.locator(f"{self._todo_list}:has-text('{task_name}')")
        """
        to_be_visible(): 这个断言会检查 locator 所指向的元素是否在页面上可见
        if completed is not None:只有当调用者明确传入了 completed 参数（True 或 False）时，才会执行这部分验证
        to_be_checked(): 断言复选框（或单选按钮）处于选中状态。
        not_to_be_checked(): 断言复选框处于未选中状态。
        """
        expect(locator).to_be_visible()

        if completed is not None:
            checkbox = locator.locator("input[type='checkbox']")
            expect(checkbox).to_be_visible()
            if completed:
                expect(checkbox).to_be_checked()
            else:
                expect(checkbox).not_to_be_checked()
