# File       : __init__.py.py
# Time       ：2024/4/2 11:57
# Author     ：nacl
# Version    ：python 3.7
# Description：日志管理器
import logging
import os
from datetime import datetime
from logging.config import dictConfig

LOG_DIR = 'logs/'
LOG_STARTSWITH = 'log-'  # log文件前缀


def config_log():
    """
    配置日志捕捉器
    @return:
    """
    log_file_name = f'{LOG_STARTSWITH}-{datetime.now().strftime("%Y%m%d")}.log'  # 文件名准确到天
    error_log_file_name = 'error-logs.log'

    log_config = {
        'version': 1,
        'formatters': {  # 日志文本格式
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
            }
        },
        'handlers': {  # 日志处理器，设置保存的文件、处理的日志等级范围、设置log文本格式等。
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'  # Ensures logging to stdout
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': os.path.join(os.getcwd(), f'{LOG_DIR}/{log_file_name}'),
                'level': logging.INFO,
                'formatter': 'default',
                'encoding': 'utf-8',  # 设置编码为 UTF-8
            },
            'error_file': {
                'class': 'logging.FileHandler',
                'filename': os.path.join(os.getcwd(), f'{LOG_DIR}/{error_log_file_name}'),
                'level': logging.ERROR,
                'formatter': 'default',
                'encoding': 'utf-8'  # 设置编码为 UTF-8
            }
        },
        'root': {  # 默认的日志记录器
            'level': 'INFO',
            'handlers': ['console', 'file']
        },
        'loggers': {  # 自定义的日志记录器
            'info_logger': {
                'level': 'INFO',
                'handlers': ['file']
            },
            'error_logger': {
                'level': 'ERROR',
                'handlers': ['error_file']
            }
        }
    }
    logging.config.dictConfig(log_config)
    clear_log()
    return log_file_name


def info(msg):
    logging.info(msg)


def error(msg):
    """
    额外输出Log到error_logger日志记录器
    @param msg:
    @return:
    """
    logging.error(msg)
    logging.getLogger('error_logger').error(msg)


def warning(msg):
    logging.warning(msg)


def clear_log(max_count=30, min_count=15):
    """
    自动清理超量的log文件，超过阈值就删除旧的log
    @param max_count: 最大文件数量
    @param min_count: 最小文件数量
    @return:
    """
    clear_excess_file(
        LOG_DIR,
        LOG_STARTSWITH,
        max_count,
        min_count
    )


def clear_excess_file(files_dir, startswith, max_count, min_count):
    """
    清除过量的文件
    :param files_dir: 目标文件夹
    :param startswith: 目标文件前缀
    :param max_count: 最大数量
    :param min_count: 最小数量
    """
    if not os.path.exists(files_dir):
        raise FileNotFoundError
    if min_count > max_count:
        raise "最大阈值比最少阈值小！"
    logs = os.listdir(files_dir)
    logs = [name for name in logs if name.startswith(startswith)]
    if len(logs) < max_count:
        return
    logs_info = [(name, os.path.getmtime(os.path.join(files_dir, name))) for name in logs]
    logs_info.sort(key=lambda x: x[1])
    for file in logs[:-min_count]:
        os.remove(os.path.join(files_dir, file))
        logging.info(f"删除超量文件，{file}")
