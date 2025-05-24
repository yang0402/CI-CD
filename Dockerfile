# 使用官方 Python 3.9 轻量版镜像作为基础
FROM python:3.9-slim

# 设置工作目录为 /app
WORKDIR /app

# 复制项目依赖文件到工作目录
COPY requirements.txt .

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码到工作目录
COPY app.py .

# 指定容器启动时运行的命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]