# File       : util.py.py
# Time       ：2024/4/8 12:07
# Author     ：nacl
# Version    ：python 3.7
# Description：基础工具方法


def try_int_string(text):
    # 尝试将字符串转成数字
    try:
        text = int(text)
        return text
    except ValueError:
        return False


def try_float_string(text):
    # 尝试将字符串转成数字
    try:
        text = float(text)
        return text
    except ValueError:
        return False
