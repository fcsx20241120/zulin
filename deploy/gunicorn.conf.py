# Gunicorn 配置文件

bind = "127.0.0.1:8000"
workers = 4  # 建议设置为 CPU 核心数 * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
threads = 2
timeout = 30
keepalive = 5

# 日志
accesslog = "/var/log/zulin/gunicorn_access.log"
errorlog = "/var/log/zulin/gunicorn_error.log"
loglevel = "info"

# 进程名
proc_name = "zulin_backend"

# 工作目录
chdir = "/var/www/zulin/backend"
