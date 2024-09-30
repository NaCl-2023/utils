# File       : test___init__.py
# Time       ：2024/4/2 12:01
# Author     ：nacl
# Version    ：python 3.7
# Description：
import time
from unittest import TestCase

from cache import Cache

cache = Cache()


@cache.func(timeout=1)
def test1():
	time.sleep(1)
	return 1111


@cache.func()
def test2(key):
	time.sleep(1)
	return 1111, key


class TestCache(TestCase):
	for _ in range(4):
		print(time.time(), test1())
		time.sleep(0.5)
	print(time.time(), test2(2))
	print(time.time(), test2(4))
	print(cache.cache)
	[print(key, str(value)) for key, value in cache.cache.items()]


