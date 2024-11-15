# File       : test__time_cache.py
# Time       ：2024/4/2 12:01
# Author     ：nacl
# Version    ：python 3.7
# Description：
from unittest import TestCase

import time_utils
from cache.time_cache import TimeCache

cache = TimeCache()


@cache.func(timeout=1)
def test_time():
    now_time = time_utils.time()
    return now_time


@cache.func()
def test_time2(key):
    time_utils.sleep(1)
    return 1111, key


class TestCache(TestCase):
    def test_check_get(self):
        """
        测试时间缓存是否有效
        @return:
        """
        start_time = time_utils.time()
        test_time()
        one_time = time_utils.time() - start_time
        start_time2 = time_utils.time()
        test_time()
        print(time_utils.time() - start_time2, one_time)
        self.assertLess(time_utils.time() - start_time2, one_time, 'check get fail')

    def test_check_timeout(self):
        res = test_time()
        time_utils.sleep(1.1)
        res2 = test_time()
        print(res, res2, time_utils.time())
        self.assertNotEqual(res, res2, 'check timeout fail')

