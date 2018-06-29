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


holidays = {}

for key in t_holidays:
    if key not in holidays:
        holidays[key] = t_holidays[key]


parser = argparse.ArgumentParser(description='Trading Day Method')
parser.add_argument('-next', '-n', type=str, dest='下一交易日，参数格式：YYYYMMDD 或 YYYY-MM-DD', default=None)
parser.add_argument('-is-trading-day', type=str, dest='' ,default=None)


def is_trading_day(dt):
    """
    判断是否为交易日，
    1、如果为周一至五，根据holidays判断，在dict中，返回False
    2、如果为周末，返回False
    3、其他情况，返回True
    :param dt:
    :return:
    """
    if type(dt) == str:
        try:
            dt = datetime.datetime.strptime(dt, '%Y%m%d')
            year = dt[0:4]
            date = dt[4:6]
        except:
            return True
    elif type(dt) == datetime.date or type(dt) == datetime.datetime:
        year = str(dt.year)
        date = '%02d' % dt.month + '%02d' % dt.day
    else:
        return True

    if dt.weekday() < 5:
        if year in holidays and date in holidays[year]:
            return False
    else:
        return False
    return True

