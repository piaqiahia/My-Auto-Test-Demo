```markdown
# 🧪 TodoMVC 自动化测试套件
本项目是一个现代化的 Web 自动化测试示例，集成了 **API 测试** 与 **UI 自动化测试**，并通过 **GitHub Actions** 实现持续集成，并自动生成美观的 **Allure 在线测试报告**。

## 🌟 核心特性

- **双重验证**: 同时覆盖后端 API 逻辑和前端 UI 交互。
- **Page Object Model (POM)**: 使用 POM 设计模式，确保 UI 测试代码高内聚、易维护。
- **Allure 报告**: 生成包含步骤、截图、日志和附件的交互式测试报告。
- **CI/CD 集成**: 通过 GitHub Actions 实现代码提交后自动运行测试并部署报告。
- **数据驱动**: 测试数据与代码分离，存放在 `YAML` 文件中，便于管理和扩展。

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https:/github.com/piaqiahia/My-Auto-Test-Demo.git
cd My-Auto-Test-Demo
```

### 2. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install
```

### 3. 本地运行测试

```bash
# 运行所有测试并生成 Allure 结果
pytest tests/ --alluredir=./allure-results

# 生成并启动本地 Allure 报告服务
allure serve ./allure-results
```

> **注意**: 请确保已安装 [Allure CLI](https://docs.qameta.io/allure-report/docs/getting-started/commandline/)。

## 📊 在线报告

每次向 `main` 分支推送代码或发起 Pull Request 时，GitHub Actions 会自动执行测试，并将 Allure 报告发布到：

👉 **[https://<your-username>.github.io/<your-repo-name>/](https://<your-username>.github.io/<your-repo-name>/)**

## 📂 项目结构

```
.
├── .github/workflows/
│   └── test.yml             # GitHub Actions CI/CD 配置文件
├── data/
│   └── todo_data.yaml       # 测试数据文件
├── logs/
│   └── app.log              # 应用日志 (运行后生成)
├── tests/
│   ├── api/
│   │   └── test_todo_api.py # API 测试用例
│   └── ui/
│       └── test_todo_ui.py  # UI 自动化测试用例
├── utils/
│   ├── api_client.py        # 封装的 API 客户端
│   ├── logger.py            # 统一日志工具
│   └── pages/
│       └── todo_page.py     # Page Object (UI 页面封装)
├── conftest.py              # Pytest 全局配置与 Fixture
├── requirements.txt         # Python 依赖列表
└── README.md                # 本文件
```

## 🤝 贡献指南

欢迎提交 Issue 或 Pull Request！在贡献前，请确保：

1.  你的代码遵循项目的编码风格。
2.  所有测试用例均已通过。
3.  更新了相关的文档（如果需要）。

## 📜 许可证

本项目基于 [MIT 许可证](LICENSE) 开源。
```

---

### ✨ 使用说明

1.  **替换占位符**:
    *   将所有的 `<your-username>` 替换为你的 GitHub 用户名。
    *   将所有的 `<your-repo-name>` 替换为你的仓库名称。
2.  **徽章 (Badges)**:
    *   第一行的两个徽章会自动从你的仓库获取状态。确保你的工作流文件名为 `test.yml`，否则需要修改链接。
3.  **在线报告链接**:
    *   确保你已经按照之前的指导，正确配置了 GitHub Pages，否则该链接会是 404。
4.  **许可证**:
    *   模板默认使用 MIT 许可证。如果你的项目使用其他许可证，请相应地修改 `LICENSE` 文件和 `README` 中的描述。

这个 `README` 不仅清晰地介绍了项目，还提供了完整的上手指南，对于任何新加入项目的开发者或审阅者来说都极其友好。