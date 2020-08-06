

```python

# 日志配置
# logger = logging.getLogger(__name__)
# formatter = TaskFormatter('%(asctime)s - %(task_id)s - %(task_name)s - %(name)s - %(levelname)s - %(message)s')
# file_handler = RotatingFileHandler(os.path.join(basedir, './PortAg/log/celery.log'),
#                                    maxBytes=10 * 1024 * 1024, backupCount=10)
# file_handler.setFormatter(formatter)
# file_handler.setLevel(logging.INFO)
# logger.addHandler(file_handler)

# logger = get_task_logger(__name__)
```