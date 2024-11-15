# File       : list_utils.py
# Time       ：2024/9/30 16:20
# Author     ：nacl
# version    ：python 3.12
# Description：数组相关工具类

def list_to_log(_list):
    """
    将数组转成日志格式
    @param _list:
    @return:
    """
    return 'size: {}, value: \n{}'.format(len(_list), '\n'.join([str(i) for i in _list])) if _list else 'None'


def list_weightlessness(_list):
    """
    数组去重，但是不改变原排序
    @param _list:
    @return:
    """
    if not isinstance(_list, list):
        raise TypeError("Input must be a list")
    seen = set()
    return [x for x in _list if not (x in seen or seen.add(x))]


def list_subtract(list1, list2):
    """
    数组相减，list1-list2
    @param list1:
    @param list2:
    @return:
    """
    if not isinstance(list1, list) and not isinstance(list2, list):
        raise TypeError("Input must be a list")
    return [i for i in list1 if i not in list2]