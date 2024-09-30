# File       : __init__.py.py
# Time       ：2024/9/30 16:14
# Author     ：junxian.guo
# version    ：python 3.8
# Description：
from datetime import datetime


def time_diff(start_time: datetime, end_time: datetime):
	# 计算两个时间的时间差，返回如23小时11分3秒
	if not start_time or not end_time:
		return 0
	if not isinstance(start_time, datetime) or not isinstance(end_time, datetime):
		return 0
	diff_time = end_time - start_time
	diffs = [
		diff_time.days,
		diff_time.total_seconds() // 60 // 60 % 60,
		diff_time.total_seconds() // 60 % 60,
		diff_time.total_seconds() % 60
	]
	diffs = [int(i) for i in diffs]
	units = ["天", "小时", "分钟", "秒"]
	diff_text = ''
	for index, diff in enumerate(diffs):
		if diff==0:
			continue
		diff_text += f'{diff}{units[index]}'
	return diff_text