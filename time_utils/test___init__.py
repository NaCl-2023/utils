# File       : test___init__.py
# Time       ：2024/11/15 18:33
# Author     ：nacl
# version    ：python 3.12


import unittest
from datetime import datetime

from time_utils import time_diff, time_format, timestamp_format


class TestTimeDiff(unittest.TestCase):

    def test_basic_functionality(self):
        start = datetime(2022, 1, 1, 12, 0, 0)
        end = datetime(2022, 1, 2, 13, 11, 3)
        expected = "1天1小时11分钟3秒"
        self.assertEqual(expected, time_diff(start, end))

    def test_zero_diff(self):
        start = datetime(2022, 1, 1, 12, 0, 0)
        end = datetime(2022, 1, 1, 12, 0, 0)
        expected = "0秒"
        self.assertEqual(expected, time_diff(start, end))

    def test_negative_diff(self):
        start = datetime(2022, 1, 1, 12, 0, 3)
        end = datetime(2022, 1, 1, 12, 0, 0)
        with self.assertRaises(ValueError):
            time_diff(start, end)

    def test_cross_day_diff(self):
        start = datetime(2022, 1, 1)
        end = datetime(2022, 1, 3, 12, 0, 0)
        expected = "2天12小时0分钟0秒"
        self.assertEqual(expected, time_diff(start, end))

    def test_type_error(self):
        start = "not a datetime object"
        end = datetime(2022, 1, 1, 12, 0, 0)
        with self.assertRaises(ValueError):
            time_diff(start, end)

    def test_time_format(self):
        time = datetime(2022, 1, 1, 12, 0, 0)
        expected = "2022-01-01 12:00:00"
        self.assertEqual(expected, time_format(time))

    def test_timestamp_format(self):
        timestamp = 1641024000
        expected = "2022-01-01 16:00:00"
        self.assertEqual(expected, timestamp_format(timestamp))


if __name__ == '__main__':
    unittest.main()
