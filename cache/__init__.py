# File       : __init__.py.py
# Time       ：2024/4/2 12:00
# Author     ：nacl
# Version    ：python 3.7
# Description：缓存相关，数据存储在字典
import functools
import time


DEFAULT_TIMEOUT = 300  # 默认过期时间


class Cache:
	def __init__(self):
		# 单个函数里用的话，应该问题不大
		self.cache: {(str, tuple): CacheData} = {}  # (func.__name__, tuple(args)): (result, save_time, timeout)

	def func(self, timeout=DEFAULT_TIMEOUT):
		# 函数的缓存，以装饰器形式使用
		def decorator(func):  # 多套一层以传参
			@functools.wraps(func)  # 将被装饰器覆盖的名字还原回来
			def wrapper(*args, **kwargs):
				_cache = self._get_data(func, args)
				if _cache:
					return _cache
				result = func(*args, **kwargs)
				self._set_data(result, func, args, timeout)
				return result

			return wrapper
		return decorator

	def _get_data(self, func, args):
		name = self._get_name(func, args)
		if name not in self.cache:
			return
		_cache: CacheData = self.cache[name]
		if _cache.save_time + _cache.timeout < time.time():
			return  # 过期了
		return _cache.data

	def _set_data(self, data, func, args, timeout):
		# 新增或覆盖数据
		name = self._get_name(func, args)
		self.cache[name] = CacheData(data, timeout)

	@staticmethod
	def _get_name(func, args):
		# 函数名和参数共同组成为索引名
		return func.__name__, tuple(args)

	def clear(self):
		self.cache.clear()


class CacheData:
	def __init__(self, data, timeout=DEFAULT_TIMEOUT):
		# 单条数据
		self.data = data
		self.timeout = timeout
		self.save_time = int(time.time())

	def __str__(self):
		return f'{self.data}, {self.save_time}, {self.timeout}'


