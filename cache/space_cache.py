# File       : __init__.py.py
# Time       ：2024/4/2 12:00
# Author     ：nacl
# Version    ：python 3.12
# Description：空间缓存
import collections
import copy
import functools
import sys

from cache import BaseData, BaseCache

DEFAULT_MAX_ONE_SIZE = 1024 * 1024 * 5  # 当条数据最大缓存，5M
DEFAULT_MAX_SUM_SIZE = 1024 * 1024 * 50  # 全部数据最大缓存，50M


class SpaceCache(BaseCache):
    """
    空间缓存
    计算大小的函数为sys.getsizeof浅计算，不会统计下层对象的大小，需要对象有__sizeof__方法。
    """
    def __init__(self):
        super().__init__()
        self.cache: {(str, tuple): Data} = collections.OrderedDict()

    def func(self, func):
        @functools.wraps(func)  # 将被装饰器覆盖的名字还原回来
        def wrapper(*args, **kwargs):
            _cache = self._get_data(func, args, kwargs)
            if _cache:
                return _cache
            result = func(*args, **kwargs)
            self._set_data(result, func, args, kwargs)
            return result

        return wrapper

    def _get_data(self, func, args, kwargs):
        name = self._get_name(func, args, kwargs)
        if name not in self.cache:
            return
        return self.cache[name].data

    def _set_data(self, data, func, args, kwargs):
        name = self._get_name(func, args, kwargs)
        _cache = Data(data)
        if _cache.size > DEFAULT_MAX_ONE_SIZE:  # 超过单条数据最大缓存，不缓存
            return
        if (self._size + _cache.size) > DEFAULT_MAX_SUM_SIZE:  # 总容量达到上限了，踢出早的几个
            # 统计那些需要删除
            old_size = copy.deepcopy(self._size)
            temp_size = 0
            end_index = 0  # 最后一个需要删除的索引
            for index, size in enumerate([data.size for data in self.cache.values()]):
                temp_size += size  # 当前容量
                if old_size + _cache.size - temp_size <= DEFAULT_MAX_SUM_SIZE:
                    end_index = index
                    break
            # 开始删除
            [self.cache.pop(key) for key in list(self.cache.keys())[:end_index+1]]
        self.cache[name] = Data(data)

    @property
    def _size(self):
        return sum([data.size for data in self.cache.values()])


class Data(BaseData):
    def __init__(self, data):
        super().__init__(data)
        self.size = sys.getsizeof(self.data)


space_cache = SpaceCache()
