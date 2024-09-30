# File       : file_tool.py
# Time       ：2024/4/8 12:13
# Author     ：nacl
# Version    ：python 3.7
# Description：涉及文件路径相关小工具
import collections
import json
import logging
import os
import re
import traceback
from configparser import ConfigParser


def convert_url(url: str):
	# 转换路径中不统一的字符
	return url.replace('\\\\', '/').replace('//', '/').replace('\\', '/')


def read_ini(url: str):
	# 读取ini文件
	if not os.path.exists(url):
		raise FileNotFoundError(url)
	conf = ConfigParser()
	conf.read(url, encoding='utf-8')
	return conf


def get_file_for_code(file, code):
	# 以特定的编码格式读取文件
	if not os.path.exists(file):
		return 'File not generated or file not found.'
	with open(file, 'r', encoding=code, errors='ignore') as f:  # 忽略编码问题
		content = f.read()

	# 去除ANSI的转义序列（颜色代码）
	if content:
		try:
			ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
			content = ansi_escape.sub('', content)
		except:
			print(traceback.format_exc())
	return content


def read_file_for_line(url):
	# 逐行读文件
	lines = []
	with open(url, 'r') as f:
		for line in f:
			lines.append(line)
	return lines


def open_json(url):
	# 打开json文件
	if not os.path.exists(url):
		raise FileNotFoundError(url)
	with open(url, 'r', encoding="utf-8") as f:
		content = json.load(f)
	return content


def open_json_order(url):
	# 打开json文件
	if not os.path.exists(url):
		raise FileNotFoundError(url)
	with open(url, 'r', encoding="utf-8") as f:
		content = f.read()
	return json.loads(content, object_pairs_hook=collections.OrderedDict)


def save_json(url, value, indent=0):
	# 保存json文件
	url = os.path.abspath(url)
	if not os.path.exists(url):
		raise FileNotFoundError(url)
	with open(url, 'w', encoding='utf-8') as f:
		f.write(json.dumps(value, indent=indent))
	return True


def get_all_file_for_dir(target_dir, file_type=None, is_abspath=False):
	# 获取目录下全部文件
	if not os.path.exists(target_dir):
		raise FileNotFoundError(target_dir)
	files = []
	for path, dirs, _files in os.walk(target_dir):
		for _file in _files:
			suffix = os.path.splitext(_file)[-1].lstrip('.')  # 后缀
			if file_type and suffix not in file_type:
				continue
			url = os.path.join(path, _file)
			files.append(url if not is_abspath else os.path.abspath(url))
	return files


def get_all_execl_for_dir(*args, **kwargs):
	# 获取目录下表格文件
	suffixes = ['xlsx', 'xlsm', 'xltx', 'xls']  # 常见表格文件后缀
	cache_prefix = '~$'  # 临时表格文件的前缀
	kwargs['file_type'] = suffixes
	res = get_all_file_for_dir(*args, **kwargs)
	return [file for file in res if not os.path.basename(file).startswith(cache_prefix)]


def save_file(url, value):
	# 保存文件
	with open(url, 'w', encoding='utf-8') as f:
		f.write(value)


def clear_excess_file(files_dir, startswith, max_count, min_count):
	"""
	清除过量的文件
	:param files_dir: 目标文件夹
	:param startswith: 目标文件前缀
	:param max_count: 最大数量
	:param min_count: 最小数量
	"""
	if not os.path.exists(files_dir):
		raise FileNotFoundError
	if min_count > max_count:
		raise "最大阈值比最少阈值小！"
	logs = os.listdir(files_dir)
	logs = [name for name in logs if name.startswith(startswith)]
	if len(logs) < max_count:
		return
	logs_info = [(name, os.path.getmtime(os.path.join(files_dir, name))) for name in logs]
	logs_info.sort(key=lambda x: x[1])
	for file in logs[:-min_count]:
		os.remove(os.path.join(files_dir, file))
		logging.info(f"删除超量文件，{file}")


def filter_file(paths):
	# 过滤路径中的非文件路径
	new_paths = []
	for path in paths:
		if os.path.isfile(path):
			new_paths.append(path)
	return new_paths
