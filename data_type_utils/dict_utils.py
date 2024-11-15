# File       : dict_utils.py
# Time       ：2024/9/30 16:19
# Author     ：nacl
# version    ：python 3.12
# Description：字典相关工具类
import copy


def deep_get(d, keys, default=None):
    """
    Get values in dictionary safely. 从多重嵌套字典中拿值
    https://stackoverflow.com/questions/25833613/safe-method-to-get-value-of-nested-dictionary

    Args:
        d (dict):
        keys (str, list): Such as `Scheduler.NextRun.value`
        default: Default return if key not found.

    Returns:

    """
    if isinstance(keys, str):
        keys = keys.split('.')
    assert type(keys) is list
    if d is None:
        return default
    if not keys:
        return d
    return deep_get(d.get(keys[0]), keys[1:], default)


def deep_set(d, keys, value):
    """
    Set value into dictionary safely, imitating deep_get(). 给多重嵌套字典赋值
    """
    if isinstance(keys, str):
        keys = keys.split('.')
    assert type(keys) is list
    if not keys:
        return value
    if not isinstance(d, dict):
        d = {}
    d[keys[0]] = deep_set(d.get(keys[0], {}), keys[1:], value)
    return d


def get_deepest_value(data: dict, depth: list = None, value_mapping: dict = None):
    """
    找到字典最深的值和keys的对应关系，递归函数
    @param data: 需要查询的字典
    @param depth: 当前纵深
    @param value_mapping: 当前映射关系
    @return:
    """
    depth = depth if depth is not None else []
    value_mapping = value_mapping if value_mapping is not None else {}
    for key, value in data.items():
        temp_depth = depth + [key]
        if isinstance(value, dict):
            get_deepest_value(value, temp_depth, value_mapping)
        else:
            value_mapping[tuple(temp_depth)] = value
    return copy.deepcopy(value_mapping)  # 只拿值，不然就id一样了


def get_deepest_value_for_layers(data: dict, layers: int, depth: list = None, value_mapping: dict = None):
    """
    找到字典最深的值和keys的对应关系，递归函数。限制遍历层数。
    @param data: 需要查询的字典
    @param layers: 遍历的层数
    @param depth: 当前纵深
    @param value_mapping: 当前映射关系
    @return:
    """
    depth = depth if depth is not None else []
    value_mapping = value_mapping if value_mapping is not None else {}
    for key, value in data.items():
        temp_depth = depth + [key]
        if isinstance(value, dict) and len(temp_depth) < layers:
            get_deepest_value_for_layers(value, layers, temp_depth, value_mapping)
        else:
            value_mapping[tuple(temp_depth)] = value
    return value_mapping  # 只拿值，不然就id一样了