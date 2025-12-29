import multiprocessing

bind = "0.0.0.0:8000"   # Azure requires this
workers = (multiprocessing.cpu_count() * 2) + 1
worker_class = "uvicorn.workers.UvicornWorker"

max_requests = 1000
max_requests_jitter = 50
timeout = 230
loglevel = "info"
accesslog = "-"
errorlog = "-"
