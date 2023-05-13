# 使用paddlepaddle/paddle:2.3.2-gpu-cuda11.2-cudnn8作为基础镜像
FROM paddlepaddle/paddle:2.3.2-gpu-cuda11.2-cudnn8

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 更新系统软件包并安装依赖项
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt .
## 改成清华 pip 源
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install --no-cache-dir -r requirements.txt

# 拷贝项目文件到工作目录
COPY . .

# 暴露端口
EXPOSE 8000

# 运行Django服务
CMD ["python3", "server/manage.py", "runserver", "0.0.0.0:8000"]
