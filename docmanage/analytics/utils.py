import calendar
from datetime import datetime
from flask import current_app
import matplotlib.pyplot as plt
import os
import pandas as pd

from docmanage.models import Order


def analyze_data_draw(bydates, order_query):
    """
    To summarize the data for table by sum, mean and count, and create and save
    graph
    :param bydates: select options by year, month, or day
    :return: array for table datas and filename of graph
    """
    # order_query = Order.query.all()
    df = pd.DataFrame([[d.order_price, d.date_order] for d in order_query],
                      columns=["order_price", "date_order"])
    # to create multi-index
    df.set_index('date_order', inplace=True)
    # filter by selected filter
    if bydates == "year":
        bydate = 'Y'
        strfInput = '%Y'
    elif bydates == "month":
        bydate = 'M'
        strfInput = '%Y/%m'
    else:
        bydate = 'D'
        strfInput = '%Y/%m/%d'
    # aggregated the data by sum, mean and count
    # print("df", df)

    df_mod = round(df.resample(bydate).agg(['sum', 'mean', 'count']))
    # cal the data for tables
    result = []
    for i, j in df_mod.iterrows():
        if int(j['order_price']['sum']) > 0:
            result.append({
                'date': i.strftime(strfInput),
                'sum': int(j['order_price']['sum']),
                'mean': int(j['order_price']['mean']),
                'count': int(j['order_price']['count'])
            })
    # its mandatory to use it for matplotlib
    # https://github.com/dghoshal-lbl/dac-man/commit/d085b9a334ee98ff4982babb11923f8c1e9eca77
    plt.switch_backend('agg')
    plt.figure()
    # use the style of grid and gray highlighted color
    plt.style.use('ggplot')
    # format fro datetime to Y-M-D
    # df_mod.index = df_mod.index.format()
    df_mod.index = df_mod.index.strftime(strfInput)
    # set the plot information
    axes = df_mod.plot(kind='bar', figsize=(10, 10), subplots=True,
                       layout=(3, 1), legend=False, color=['lightblue'],
                       title='Orders by ' + bydates)
    # set the title and ylabel by each graphs
    axes[0][0].set(title='order_sum', ylabel='order-sum($)')
    axes[1][0].set(title='order_average', ylabel='order_average($)')
    axes[2][0].set(title='order_count', ylabel='order_count')
    # format to the comma for digits
    axes[0][0].yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    axes[1][0].yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    # save file name
    filename = 'plot.png'
    # os.path.join can track the location of the working folders
    # to save the file
    plt.savefig(os.path.join(current_app.root_path, 'static/images', filename))
    # plt.close('all')
    return result, filename
"""
# test
    df['year'] = df['date_order'].dt.year
    df['month'] = df['date_order'].dt.month
    df['day'] = df['date_order'].dt.day

    # df_mod = df.groupby(['year']).order_price.agg(['mean', 'sum', 'count'])
    # df_mod = df.groupby(['year', 'month']).order_price.agg(['mean', 'sum', 'count'])
    df_mod = df.groupby(['year', 'month', 'day']).order_price.agg(['mean', 'sum', 'count'])
    # https://note.nkmk.me/python-pandas-plot/
    print(df_mod)
    plt.switch_backend('agg')
    plt.figure()
    # df_mod.plot(subplots=True)
    df_mod.plot.bar(subplots=True)
    filename='test.png'
    plt.savefig(os.path.join(current_app.root_path, 'static/images', filename))
    plt.close('all')
    # print(df_mod.loc[(2020)].sum())
    # print(df_mod.loc[(2020, 5)].sum())
    # print(df_mod.loc[(2020, 5)])

    # res = df_mod.to_xarray().to_array()
    # print(res)

###
"""


def cal_days():
    """
    To get and return the data for 30 days of today
    :return: order_query
    """
    today = datetime.today()
    year = today.year
    month = today.month
    last_day = calendar.monthrange(int(year), int(month))[1]
    start = datetime(year=int(year), month=int(month), day=1)
    end = datetime(year=int(year), month=int(month), day=last_day)
    order_query = Order.query.filter(Order.date_order <= end) \
        .filter(Order.date_order >= start) \
        .order_by(Order.date_order.desc()) \
        .all()
    return order_query


def cal_months():
    """
    To get and return the data for 30 days of today
    :return: order_query
    """
    today = datetime.today()
    lastyear = today.year-1
    thisyear = today.year
    lastmonth = today.month+1
    thismonth = today.month
    last_day = calendar.monthrange(int(thisyear), int(thismonth))[1]
    start = datetime(year=int(lastyear), month=int(lastmonth), day=1)
    end = datetime(year=int(thisyear), month=int(thismonth), day=last_day)
    order_query = Order.query.filter(Order.date_order <= end) \
        .filter(Order.date_order >= start) \
        .order_by(Order.date_order.desc()) \
        .all()
    return order_query


def cal_years():
    """
    To get and return the data for 30 days of today
    :return: order_query
    """
    today = datetime.today()
    lastyear = today.year-9
    thisyear = today.year
    lastmonth = today.month+1
    thismonth = today.month
    last_day = calendar.monthrange(int(thisyear), int(thismonth))[1]
    start = datetime(year=int(lastyear), month=int(lastmonth), day=1)
    end = datetime(year=int(thisyear), month=int(thismonth), day=last_day)
    order_query = Order.query.filter(Order.date_order <= end) \
        .filter(Order.date_order >= start) \
        .order_by(Order.date_order.desc()) \
        .all()
    return order_query
