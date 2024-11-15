# File       : test__space_cache.py
# Time       ：2024/4/2 12:01
# Author     ：nacl
# Version    ：python 3.12
# Description：
from dataclasses import dataclass
from unittest import TestCase

import time
from space_cache import space_cache, DEFAULT_MAX_ONE_SIZE


@dataclass
class Test:
    size: int

    def __sizeof__(self):
        return int(self.size)


@space_cache.func
def test_size(size, key = None):
    return Test(size)


@space_cache.func
def test_get():
    time.sleep(1)
    return Test(1)


class TestCache(TestCase):
    def test_check_get(self):
        """
        测试空间缓存是否有效
        @return:
        """
        start_time = time.time()
        test_get()
        one_time = time.time() - start_time
        start_time2 = time.time()
        test_get()
        print(time.time() - start_time2, one_time)
        self.assertLess(time.time() - start_time2, one_time, 'check get fail')

    def test_check_sum_max(self):
        space_cache.clear()
        for i in range(20):  # 50M
            test_size(DEFAULT_MAX_ONE_SIZE * 0.5, key=i)  # 2.5M
        print(space_cache._size, space_cache._size / 1024 / 1024)  # 47.5
        test_size(DEFAULT_MAX_ONE_SIZE / 5 * 3, key=-1)  # 3M
        print(space_cache._size, space_cache._size / 1024 / 1024)  # 47.5 - 2.5 + 3 = 48
        self.assertEqual(int(space_cache._size / 1024 / 1024), 48, 'check pop one fail')
        test_size(DEFAULT_MAX_ONE_SIZE, key=-3)  # 5M
        print(space_cache._size, space_cache._size / 1024 / 1024)  # 48 - 2.5 - 2.5 + 5 = 48
        self.assertEqual(int(space_cache._size / 1024 / 1024), 48, 'check pop move fail')

    def test_check_one_max(self):
        old_size = space_cache._size
        test_size(DEFAULT_MAX_ONE_SIZE + 1)
        print(space_cache._size, space_cache.cache.keys())
        self.assertEqual(space_cache._size, old_size, 'check one max fail')
