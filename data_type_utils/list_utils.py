# File       : list_utils.py
# Time       ：2024/9/30 16:20
# Author     ：junxian.guo
# version    ：python 3.8
# Description：数组相关工具类

def list_to_log(_list):
    # 将数组转成text
    return 'size: {}, value: \n{}'.format(len(_list), '\n'.join([str(i) for i in _list])) if _list else 'None'


def list_weightlessness(_list):
    # 数组去重，但是不改变原排序
    return sorted(list(set(_list)), key=_list.index)


def list_subtract(list1, list2):
    # 数组相减,list1-list2
    return [i for i in list1 if i not in list2]