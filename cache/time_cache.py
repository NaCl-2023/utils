# File       : time_cache.py
# Time       ：2024/11/15 15:11
# Author     ：nacl
# version    ：python 3.12
# Description：时间缓存
import functools
import time

from . import BaseCache, BaseData

DEFAULT_TIMEOUT = 300  # 默认过期时间


class TimeCache(BaseCache):

    def func(self, timeout=DEFAULT_TIMEOUT):
        """
        函数缓存装饰器
        @param timeout: 超时时间
        @return:
        """

        def decorator(func):  # 多套一层以传参
            @functools.wraps(func)  # 将被装饰器覆盖的名字还原回来
            def wrapper(*args, **kwargs):
                _cache = self._get_data(func, args, kwargs)
                if _cache:
                    return _cache
                result = func(*args, **kwargs)
                self._set_data(result, func, args, kwargs, timeout)
                return result

            return wrapper

        return decorator

    def cls(self, cls, timeout=DEFAULT_TIMEOUT):
        """
        类装饰器，用于缓存类的实例化结果
        @param cls:
        @param timeout: 超时时间
        :return:
        """

        @functools.wraps(cls)
        def wrapper(*args, **kwargs):
            _cache = self._get_data(cls, args, kwargs)
            if _cache:
                return _cache
            result = cls(*args, **kwargs)
            self._set_data(result, cls, args, kwargs, timeout)
            return result

        class CachedClass(cls):
            def __new__(cls, *args, **kwargs):
                return wrapper(*args, **kwargs)

        CachedClass.__name__ = cls.__name__
        CachedClass.__doc__ = cls.__doc__
        CachedClass.__module__ = cls.__module__
        CachedClass.__qualname__ = cls.__qualname__

        # 将原始类的属性和方法复制到新类中
        for attr_name in dir(cls):
            if not attr_name.startswith('__'):
                attr = getattr(cls, attr_name)
                if callable(attr):
                    setattr(CachedClass, attr_name, attr)

        return CachedClass

    def _get_data(self, func, args, kwargs):
        name = self._get_name(func, args, kwargs)
        if name not in self.cache:
            return
        _cache: CacheData = self.cache[name]
        if _cache.is_timeout:
            return  # 过期了
        return _cache.data

    def _set_data(self, data, func, args, kwargs, timeout):
        name = self._get_name(func, args, kwargs)
        self.cache[name] = CacheData(data, timeout)


class CacheData(BaseData):
    def __init__(self, data, timeout: int):
        super().__init__(data)
        self.timeout = timeout
        self.save_time = int(time.time())
        self.check_timeout()  # 校验超时时间

    def check_timeout(self):
        if not self.timeout:
            raise ValueError('timeout is None')
        if not isinstance(self.timeout, (int, float)):
            raise ValueError('timeout is not int or float')
        if self.timeout <= 0:
            raise ValueError('timeout is less than or equal to 0')

    @property
    def is_timeout(self):
        return (self.save_time + self.timeout) < time.time()


time_cache = TimeCache()
