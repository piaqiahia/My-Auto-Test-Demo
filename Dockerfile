# 使用官方 Playwright Python 镜像（已含 Chromium）
FROM mcr.microsoft.com/playwright/python:v1.58.0

# 设置时区和非交互模式
ENV DEBIAN_FRONTEND=noninteractive TZ=Asia/Shanghai

# 安装 JMeter 和 Allure（使用国内源加速）
RUN sed -i 's|http://[a-z0-9\.]*\.archive\.ubuntu\.com|https://mirrors.aliyun.com|g' /etc/apt/sources.list && \
    sed -i 's|http://security\.ubuntu\.com|https://mirrors.aliyun.com|g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jdk wget ca-certificates && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# 安装 JMeter（阿里云镜像）
ARG JMETER_VERSION=5.6.3
RUN wget -q --timeout=30 --tries=3 https://mirrors.aliyun.com/apache/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz -P /tmp && \
    tar -xzf /tmp/apache-jmeter-${JMETER_VERSION}.tgz -C /opt && \
    ln -s /opt/apache-jmeter-${JMETER_VERSION}/bin/jmeter /usr/local/bin/jmeter && \
    rm /tmp/apache-jmeter-${JMETER_VERSION}.tgz

# 安装 Allure（GitHub 官方包）
ARG ALLURE_VERSION=2.29.0
RUN wget -q --timeout=30 --tries=3 https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz -P /tmp && \
    tar -xzf /tmp/allure-${ALLURE_VERSION}.tgz -C /opt && \
    ln -s /opt/allure-${ALLURE_VERSION}/bin/allure /usr/local/bin/allure && \
    rm /tmp/allure-${ALLURE_VERSION}.tgz

# 验证
RUN java -version && jmeter --version && allure --version

# 设置 PATH
ENV PATH=$PATH:/opt/apache-jmeter-${JMETER_VERSION}/bin:/opt/allure-${ALLURE_VERSION}/bin

# 安装 Python 依赖
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt

# 复制项目
COPY . .

# 创建目录
RUN mkdir -p logs reports/allure_results

# 暴露端口（可选）
EXPOSE 1099 4445 50000

# 启动命令
CMD ["python", "run_all.py"]