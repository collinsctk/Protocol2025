#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

# https://foofish.net/python-decorator.html

from functools import wraps
from datetime import datetime


def print_run_time():

    def decorator(func):
        @wraps(func)  # 保持func.__name__ func.__doc__
        def run_func(*args, **kwargs):  # (*args, **kwargs) 可以接受任意参数
            start_time = datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.now()
            # 1000000 microsecond = 1 second
            print(f'运行时间: {(end_time - start_time).microseconds} 微秒')
            # 装饰器添加的功能
            return result  # 返回函数
        return run_func  # 返回函数 + 写入返回内容到文件
    return decorator  # 返回函数 + 写入返回内容到文件 + 保持func.__name__ func.__doc__


if __name__ == '__main__':
    pass
