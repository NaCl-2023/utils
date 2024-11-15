# File       : log_decorator.py
# Time       ：2024/9/26 12:21
# Author     ：nacl
# version    ：python 3.12
# Description：日志装饰器
import functools
import logging


def log(func):
    """
    常规函数log装饰器
    @param func:
    @return:
    """
    name = '[Log Decorator]'

    @functools.wraps(func)  # 将被装饰器覆盖的名字还原回来
    def wrapper(*args, **kwargs):
        text = f"{name} Calling function [{func.__name__}] with arguments: [{args}, {kwargs}]"
        logging.info(text if len(text) < 200 else text[:200] + '...]')
        result = func(*args, **kwargs)
        text = f"{name} Function [{func.__name__}] returned: [{result}]"
        logging.info(text if len(text) < 200 else text[:200] + '...]')
        return result

    return wrapper


def log_mongodb(func):
    """
    Mongodb日志装饰器
    @param func:
    @return:
    """
    pass

def log_request(func):
    """
    web请求装饰器
    @param func:
    @return:
    """
    pass
