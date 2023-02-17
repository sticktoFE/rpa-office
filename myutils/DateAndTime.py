# 装饰器，用于测量阻塞计时
import functools
import time

# 装饰器，用于计时


def clock(func):
    @functools.wraps(func)
    def caltime(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        time_cost = end_time - start_time
        print(f"模块{func.__module__}--方法{func.__name__}，用时{time_cost}")
        return res
    return caltime
