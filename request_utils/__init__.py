# File       : __init__.py
# Time       ：2024/10/2 21:18
# Author     ：author name
# version    ：python 3.12.3
# Description：请求数据
import functools

from flask import request, jsonify  # 仅适用于flask


def check_age(has_args):
    """
    检查请求参数，检查是否穿过来了、是否有值
    @param has_args: 需要的参数
    @return:
    """
    def inner_wrapper(func):
        @functools.wraps(func)
        def wrapper():
            ages = get_age()
            if has_args and not ages:
                return jsonify({"success": False, 'msg': '无传递参数，请检查！'})
            if has_args:
                for key in has_args:
                    if key not in ages:
                        return jsonify({"success": False, 'msg': f'缺少参数{key}，请检查！'})
                    if ages[key] in ['', None]:
                        return jsonify({"success": False, 'msg': f'参数{key}不存在值，请检查！'})

            return func()
        return wrapper
    return inner_wrapper


def get_age() -> dict:
    """
    获取get和post参数
    @return:
    """
    return dict(request.args) if request.method.upper() == 'GET' else dict(request.form)



