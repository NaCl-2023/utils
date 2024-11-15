# File       : __init__.py.py
# Time       ：2024/4/2 11:39
# Author     ：nacl
# Version    ：python 3.7
# Description：定时器和定时器装饰器
import functools
import threading
from typing import Optional


class LoopTimer:
    def __init__(self, interval, times, func, *args, **kwargs):
        """
        循环定时器，默认先运行一次
        Args:
            interval: 间隔，单位秒
            times: 次数，-1为永久
            func: 执行的函数
        """
        self.interval: int = interval
        self.times: int = times
        self.func = func

        self.args = args
        self.kwargs = kwargs

        self.timer: Optional[threading.Timer] = None

    def run(self):
        self.func(*self.args, **self.kwargs)
        self._end()

    def _end(self):
        self.times -= 1
        if self.times == -1 or self.times > 0:
            self.timer = threading.Timer(self.interval, self.run)
            self.timer.start()

    def start(self, is_run=True):
        if is_run:
            self.func(*self.args, **self.kwargs)
        else:
            self.times += 1
        self._end()

    def stop(self):
        self.timer.cancel()
        self.timer = 0


class LoopTimerDec(LoopTimer):
    """
    循环定时器装饰器
    Args:
        interval: 间隔，单位秒
        times: 次数，-1为永久
        func: 执行的函数
    """

    def __init__(self, *args, **kwargs):
        super().__init__(int(), int(), int(), *args, **kwargs)

    def decorator(self, interval, times, is_run=True):
        self.interval = interval
        self.times = times

        def decorator2(func):  # 多套一层以传参
            @functools.wraps(func)  # 将被装饰器覆盖的名字还原回来
            def wrapper(*args, **kwargs):
                self.func = func
                self.args = args
                self.kwargs = kwargs
                if is_run:
                    self.func(*self.args, **self.kwargs)
                else:
                    self.times += 1
                self._end()
                return self  # 被执行的函数不应该有返回，固定返回定时器

            return wrapper

        return decorator2
