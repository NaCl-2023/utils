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


def convert_path(path: str):
    """
    转换路径中不统一的字符
    @param path:
    @return:
    """
    return os.path.normpath(path).replace('\\', '/')


def read_ini(path: str):
    """
    读取ini文件
    @param path:
    @return:
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    conf = ConfigParser()
    conf.read(path, encoding='utf-8')
    return conf


def get_file_for_code(file, code):
    """
    以特定的编码格式读取文件
    @param file:
    @param code:
    @return:
    """
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


def read_file_for_line(path):
    """
    逐行读文件
    @param path:
    @return:
    """
    lines = []
    with open(path, 'r') as f:
        for line in f:
            lines.append(line)
    return lines


def open_json(path, encoding='utf-8'):
    """
    打开json文件
    @param path:
    @param encoding:
    @return:
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    try:
        with open(path, 'r', encoding=encoding) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON from {path}: {e}")


def open_json_back_order(path, encoding='utf-8'):
    """
    打开json文件，返回有序字典collections.OrderedDict
    @param path:
    @param encoding:
    @return:
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    try:
        with open(path, 'r', encoding=encoding) as f:
            return json.load(f, object_pairs_hook=lambda pairs: collections.OrderedDict(pairs))
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON from {path}: {e}")


def save_json(url, value, indent=0):
    """
    保存json文件
    @param url:
    @param value:
    @param indent: 空格
    @return:
    """
    url = os.path.abspath(url)
    if not os.path.exists(url):
        raise FileNotFoundError(url)
    with open(url, 'w', encoding='utf-8') as f:
        f.write(json.dumps(value, indent=indent))
    return True


def get_all_file_for_dir(target_dir, type_filter: list=None, is_abspath=False):
    """
    获取目录下全部文件
    @param target_dir:
    @param type_filter: 类型过滤
    @param is_abspath:
    @return:
    """
    if not os.path.exists(target_dir):
        raise FileNotFoundError(target_dir)
    if type_filter is None:
        type_filter = []
    elif not isinstance(type_filter, list):
        type_filter = [type_filter]

    target_files = []
    for root, _, files in os.walk(target_dir):
        for file in files:
            suffix = os.path.splitext(file)[-1].lstrip('.').lower()  # 后缀
            if type_filter and suffix not in type_filter:
                continue
            target_files.append(file if not is_abspath else os.path.abspath(os.path.join(root, file)))
    return target_files


def save_file(url, value):
    """
    保存文件
    @param url:
    @param value:
    @return:
    """
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
    """
    过滤路径中的非文件路径
    @param paths:
    @return:
    """
    new_paths = []
    for path in paths:
        if os.path.isfile(path):
            new_paths.append(path)
    return new_paths


def open_file_for_offset(url, offset: int = 0):
    """
    使用偏移值读文件部分内容
    @param url: 文件
    @param offset: 偏移值
    @return: 内容和最后的偏移值
    """
    if not os.path.exists(url):
        raise IOError(f'No found {url}!')
    with open(url, 'r') as f:
        f.seek(offset)
        return f.read(), f.tell()
