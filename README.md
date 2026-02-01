# README.md

```markdown
# 🧪 全栈自动化测试演示项目

> 一个集 **API 测试**、**UI 自动化** 与 **性能压测** 于一体的端到端自动化测试框架，适用于 Web 应用的质量保障。本项目采用 Python + Playwright + Pytest + Allure + JMeter 技术栈，并集成 GitHub Actions 实现 CI/CD。

---

## 项目亮点

- **三层测试覆盖**：API 接口测试 + Web UI 自动化 + JMeter 性能压测
- **Page Object Model (POM)** 架构，提升 UI 测试可维护性
- **Allure 可视化报告**：含步骤追踪、失败截图、API 响应附件
- **一键执行脚本** (`run_all.py`)：自动运行全部测试并生成报告
- **Docker 支持**：通过 `docker-compose` 快速搭建测试环境
- **GitHub Actions CI/CD**：代码推送后自动测试并发布报告至 GitHub Pages

---

## 项目结构

```
├── .github/workflows/
│   └── mygithub.yml         # GitHub Actions CI/CD 配置
├── data/
│   └── todo_data.yaml       # 测试数据（YAML 格式）
├── jmeter_script/           # JMeter 脚本与测试数据
│   ├── View_Results_Tree1.jmx
│   └── users.csv
├── logs/                    # 运行时生成的日志文件
├── reports/                 # 测试报告输出目录
│   ├── allure_report        # Allure HTML 报告
│   └── jmeter_report        # JMeter Dashboard 报告
├── tests/
│   ├── api/                 
│       └── test_todo_api.py # API 测试用例
│   └── ui/                  # UI 自动化测试用例
│       └── pages/           # Page Object 封装
├── utils/
│   ├── api_client.py        # 封装的 HTTP 客户端
│   └── logger.py            # 统一日志工具
├── conftest.py              # Pytest 全局配置与 Fixture
├── run_all.py               # 一体化测试执行入口
├── dockerfile               # 镜像生成流程
├── docker-compose.yml       # Docker 环境定义
└── requirements.txt         # Python 依赖列表
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
playwright install --with-deps  # 安装浏览器驱动
```

> **注意**：需提前安装 [JMeter](https://jmeter.apache.org/) 并配置到 `PATH`。

### 2. 本地运行全部测试

```bash
python run_all.py
```

执行后将：
- 运行 `tests/` 下所有 Pytest 用例（含 API 与 UI）
- 生成 Allure 原始结果 → 转换为 HTML 报告（`reports/allure_report/index.html`）
- 执行 JMeter 脚本 → 生成性能报告（`reports/jmeter_report/index.html`）

### 3. 查看报告

- **Allure 报告**：打开 `reports/allure_report/index.html`
- **JMeter 报告**：打开 `reports/jmeter_report/index.html`
- **日志**：查看 `logs/app.log`

---

## Docker 支持

使用 Docker Compose 启动测试环境（含 Allure 实时服务）：

```bash
docker-compose up --build
```

- Allure 报告服务：`http://localhost:5050`
- 测试结果会自动同步到 `./allure-results`

---

##  CI/CD 流程（GitHub Actions）

当向 `master` 分支推送代码或发起 PR 时，自动触发以下流程：

1. 安装 Python、Playwright、JMeter、Allure CLI
2. 并行执行：
   - Pytest 测试（生成 Allure 结果）
   - JMeter 性能测试（生成 JTL 日志）
3. 生成 Allure 与 JMeter HTML 报告
4. 将报告部署到 **GitHub Pages**（路径：`/allure` 和 `/jmeter`）

> 报告访问地址：`https://piaqiahia.github.io/My-Auto-Test-Demo/allure`
> 及`https://piaqiahia.github.io/My-Auto-Test-Demo/jmeter`

---

## 技术栈

| 类别 | 工具 |
|------|------|
| 编程语言 | Python 3.11+ |
| UI 自动化 | Playwright |
| 测试框架 | Pytest |
| API 测试 | requests + httpbin.org |
| 报告生成 | Allure |
| 性能测试 | Apache JMeter |
| CI/CD | GitHub Actions |
| 容器化 | Docker / Docker Compose |

---

## 适用场景

- 团队自动化测试框架参考
- 学习 Playwright + Allure + JMeter 集成实践

---

> **让自动化测试更简单、更可靠、更可视化！**
```