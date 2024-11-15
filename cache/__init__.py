# File       : __init__.py.py
# Time       ：2024/4/2 12:00
# Author     ：nacl
# Version    ：python 3.12
# Description：缓存基础类
from hashlib import md5


class BaseCache:
    cache: {(str, tuple): object} = {}

    def func(self, *args, **kwargs):
        """
        函数缓存装饰器
        @return:
        """
        pass

    def _get_data(self, *args, **kwargs):
        pass

    def _set_data(self, *args, **kwargs):
        pass

    @staticmethod
    def _get_name(func, args, kwargs):
        """
        函数名和参数共同组成为索引key，参数str化并转成md5
        @param func: 函数
        @param args: 参数
        @param kwargs: key参数
        @return:
        """
        m = md5()
        m.update((str(args) + str(kwargs)).encode('utf-8'))
        return func.__name__, m.hexdigest()

    def clear(self):
        self.cache.clear()


class BaseData:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()
