# File       : __init__.py.py
# Time       ：2024/9/30 16:14
# Author     ：nacl
# version    ：python 3.12
# Description：
from datetime import datetime


def time_format(time: datetime, format_str: str = "%Y-%m-%d %H:%M:%S"):
    """
    时间格式化
    @param time:
    @param format_str:
    @return:
    """
    if not time:
        raise ValueError("Time must exist")
    if not isinstance(time, datetime):
        raise ValueError("Time must be a datetime object")
    return time.strftime(format_str)


def timestamp_format(timestamp: int, format_str: str = "%Y-%m-%d %H:%M:%S"):
    """
    时间戳格式化
    @param timestamp:
    @param format_str:
    @return:
    """
    if not timestamp:
        raise ValueError("Timestamp must exist")
    if not isinstance(timestamp, int):
        raise ValueError("Timestamp must be a int object")
    return datetime.fromtimestamp(timestamp).strftime(format_str)


def time_diff(start_time: datetime, end_time: datetime):
    """
    计算两个时间的时间差，返回如23小时11分3秒
    @param start_time:
    @param end_time:
    @return:
    """
    if not start_time or not end_time:
        raise ValueError("Both start_time and end_time must exist!")
    if not isinstance(start_time, datetime) or not isinstance(end_time, datetime):
        raise ValueError("Both start_time and end_time must be datetime objects!")
    diff_time = end_time - start_time
    if diff_time.days < 0:
        raise ValueError("Start_time is greater than end_time!")
    if diff_time.total_seconds() == 0:
        return "0秒"
    diff_mapping = [
        (diff_time.days, "天"),
        (diff_time.total_seconds() // 60 // 60 % 24, "小时"),
        (diff_time.total_seconds() // 60 % 60, "分钟"),
        (diff_time.total_seconds() % 60, "秒")
    ]
    diff_text = ''
    for diff, unit in diff_mapping:
        if diff >= 0:
            diff_text += f'{int(diff)}{unit}'
    return diff_text
