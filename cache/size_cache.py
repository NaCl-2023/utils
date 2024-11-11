# File       : __init__.py.py
# Time       ：2024/4/2 12:00
# Author     ：junxian.guo
# Version    ：python 3.8
# Description：缓存相关，数据存储在字典
import collections
import functools
import sys
from hashlib import md5

DEFAULT_MAX_ONE_SIZE = 1024 * 1024 * 5  # 当条数据最大缓存，5M
DEFAULT_MAX_SUM_SIZE = 1024 * 1024 * 50  # 全部数据最大缓存，50M


class SizeCache:
    """
    空间缓存
    计算大小的函数为sys.getsizeof浅计算，不会统计下层对象的大小，需要对象有__sizeof__方法。
    """

    def __init__(self):
        # 有序字典 (func.__name__, tuple(args)): (result, save_time, timeout)
        self.cache: {(str, tuple): CacheData} = collections.OrderedDict()

    def func(self):
        # 函数的缓存，以装饰器形式使用
        def decorator(func):  # 多套一层以传参
            @functools.wraps(func)  # 将被装饰器覆盖的名字还原回来
            def wrapper(*args, **kwargs):
                _cache = self._get_data(func, args, kwargs)
                if _cache:
                    return _cache
                result = func(*args, **kwargs)
                self._set_data(result, func, args, kwargs)
                return result

            return wrapper

        return decorator

    def _get_data(self, func, args, kwargs):
        name = self._get_name(func, args, kwargs)
        if name not in self.cache:
            return
        _cache: CacheData = self.cache[name]
        return _cache.data

    def _set_data(self, data, func, args, kwargs):
        # 新增或覆盖数据
        name = self._get_name(func, args, kwargs)
        _cache = CacheData(data)
        if _cache.size > DEFAULT_MAX_ONE_SIZE:
            return
        if self._size > DEFAULT_MAX_SUM_SIZE:
            # 总容量达到上限了，踢出早的几个
            # 统计那些需要删除
            temp_size = 0
            end_index = 0  # 最后一个需要删除的索引
            for index, size in enumerate([data.size for data in self.cache.values()]):
                temp_size += size  # 当前容量
                if _cache.size < temp_size:
                    end_index = index
                    break

            # 开始删除
            for key in list(self.cache.keys())[:end_index]:
                self.cache.pop(key)

        self.cache[name] = CacheData(data)

    @staticmethod
    def _get_name(func, args, kwargs):
        # 函数名和参数共同组成为索引名，参数str化并转成md5
        m = md5()
        m.update((str(args)+str(kwargs)).encode('utf-8'))
        return func.__name__, m.hexdigest()

    @property
    def _size(self):
        return sum([data.size for data in self.cache.values()])

    def clear(self):
        self.cache.clear()


class CacheData:
    def __init__(self, data):
        # 单条数据
        self.data = data
        self.size = sys.getsizeof(self.data)

    def __str__(self):
        return f'{self.data}, {self.size}'

    def __repr__(self):
        return self.__str__()


cache = SizeCache()
