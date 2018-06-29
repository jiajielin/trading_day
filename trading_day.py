"""
author: Jia Jielin
time: 2018/4/2 17:44
desc:

"""
import datetime
import json
import argparse
import sys

HOLIDAYS_FILE = 'holidays.json'

# 文件
try:
    with open(HOLIDAYS_FILE) as f:
        t_holidays = json.load(f)
        for key in t_holidays:
            t_holidays[key] = t_holidays[key].split(';')
except:
    t_holidays = {}


def next_trading_day(dt):
    """
    :param dt:字符串 YYYYMMDD 或 YYYY-MM-DD，或datetime/date
    :return: 下一个交易日 返回类型与dt类型相同
    """
    format_flag = -1 # 0:YYYYMMDD;1:YYYY-MM-DD;-1:datetime/date
    if type(dt) == str:
        try:
            dt = datetime.datetime.strptime(dt, '%Y%m%d')
            format_flag = 0
        except:
            try:
                dt = datetime.datetime.strptime(dt, '%Y-%m-%d')
                format_flag = 1
            except:
                return '0'
    elif type(dt) == datetime.date or type(dt) == datetime.datetime:
        format_flag = -1
    else:
        return '0'

    counter = 30
    next_day = dt + datetime.timedelta(days=1)
    while( is_trading_day(next_day) == 0 and counter):
        next_day = next_day + datetime.timedelta(days=1)
        counter -= 1
    if format_flag == 0:
        return next_day.strftime('%Y%m%d')
    elif format_flag == 1:
        return next_day.strftime('%Y-%m-%d')
    else:
        return next_day


def is_trading_day(dt):
    """
    判断是否为交易日，
    1、如果为周一至五，根据holidays判断，在dict中，返回0
    2、如果为周末，返回0
    3、其他情况，返回1
    :param dt:
    :return: 0/1/-1
    """
    if type(dt) == str:
        try:
            dt = datetime.datetime.strptime(dt, '%Y%m%d')
        except:
            try:
                dt = datetime.datetime.strptime(dt, '%Y-%m-%d')
            except:
                return -1
    elif type(dt) == datetime.date or type(dt) == datetime.datetime:
        pass
    else:
        return -1

    year = str(dt.year)
    date = '%02d' % dt.month + '%02d' % dt.day

    if dt.weekday() < 5:
        if year in holidays and date in holidays[year]:
            return 0
    else:
        return 0
    return 1

holidays = {}

for key in t_holidays:
    if key not in holidays:
        holidays[key] = t_holidays[key]
# 输入日期为输入为datetime或str(YYYY-MM-DD YYYYMMDD
# -n\--next: 跟日期，返回下一个交易日
# -t\--trading-day: 跟日期，返回0或1
parser = argparse.ArgumentParser('trading method', description='交易日相关命令')
parser.add_argument('-next', '-n', type=str, help='下一交易日，参数格式：YYYYMMDD 或 YYYY-MM-DD，返回格式与输入格式相同', default=None)
parser.add_argument('-is-trading-day', '-t', type=str, help='是否为交易日，参数格式：YYYYMMDD 或 YYYY-MM-DD，是交易日返回1，否则返回0，格式错误-1', default=None)

args = parser.parse_args()
if args.next:
    sys.exit(next_trading_day(args.next))
elif args.is_trading_day:
    sys.exit(is_trading_day(args.is_trading_day))




