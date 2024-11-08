# File       : test___init__.py
# Time       ：2024/4/2 12:01
# Author     ：nacl
# Version    ：python 3.7
# Description：
from dataclasses import dataclass
from unittest import TestCase

from size_cache import SizeCache

cache = SizeCache()


@dataclass
class Test:
    size: int

    def __sizeof__(self):
        return self.size


@cache.func()
def test1():
    return Test(1024 * 1024 * 6 + 1)


@cache.func()
def test2(key):
    return Test(1024 * 1024 * 4)


class TestCache(TestCase):
    for index in range(15):
        _ = test2(index)
        print(cache._size, cache.cache.keys())
    test1()
    print(cache._size, cache.cache.keys())
