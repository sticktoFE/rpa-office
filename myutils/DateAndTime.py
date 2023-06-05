# 装饰器，用于测量阻塞计时
import functools
import time

# 设置获取数据的日期
from datetime import date, datetime, timedelta


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


# start_date = datetime(2023, 1, 2)
# end_date = datetime(2023, 12, 31)

# delta = relativedelta(end_date, start_date)
# num_weeks = (delta.years * 52) + delta.weeks

# for week in range(num_weeks):
#     week_start = start_date + relativedelta(weeks=week)
#     week_end = week_start + relativedelta(days=6)
#     print("Week {} ({} - {})".format(week + 1, week_start.date(), week_end.date()))


# week_num = start_date.isocalendar()[1]

# while start_date <= end_date:
#     print(
#         "Week {} ({}) - {}".format(
#             week_num,
#             start_date.strftime("%m/%d/%Y"),
#             (start_date + timedelta(days=6)).strftime("%m/%d/%Y"),
#         )
#     )
#     start_date += timedelta(days=7)
#     week_num += 1


def get_weeks_current_date(date_str=None, week_start_delt_days=-3, week_days=7):
    """
    获取传入日期所在本年度中的周数，及起始和结束日
    """
    current_date = None
    if date_str is None:
        current_date = datetime.today()
    else:
        current_date = datetime.strptime(date_str, "%Y-%m-%d")
    week_num = current_date.isocalendar()[1]
    # 默认一周的开始为周一，如果自定义周的起始日，如果周二，就+1，如果上周日就-1，上周五开始的话就-3
    start_date = (
        current_date - timedelta(days=current_date.weekday()) + timedelta(days=-3)
    )
    end_date = start_date + timedelta(days=week_days - 1)
    format_week = (
        f'{start_date.strftime("%m%d")}-{end_date.strftime("%m%d")}({week_num})'
    )
    return (
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d"),
        format_week,
    )


# 获取时间字符串，type为0表示今天，昨天是-1 明天是1 以此类推
def get_date(type=0, format="%Y-%m-%d"):
    today = date.today()
    if type >= 0:
        reurn_date = today + timedelta(days=type)
    else:
        reurn_date = today - timedelta(days=-type)
    return datetime.strftime(reurn_date, format)


if __name__ == "__main__":
    print(get_weeks_current_date())
