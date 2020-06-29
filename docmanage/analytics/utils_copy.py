import os
from docmanage.models import Order
from flask import current_app
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# It is old function not to be used below
def analyze_data(byDates):
    """
    To analyze the data of reports by year, month, or day
    :param byDates: filter by year, month, or day
    :return: data filterd by year, month or day
    """
    test_query = Order.query.all()
    df = pd.DataFrame([[d.order_price, d.date_order] for d in test_query],
                      columns=["order_price", "date_order"])

    # test0
    # month_df = df.groupby(df['date_order'].dt.strftime('%B'))['order_price'].sum()
    # print("month", month_df)
    # year_df = df.groupby(df['date_order'].dt.strftime('%y'))['order_price'].sum()
    # print(year_df)
    # day_df = df.groupby(df['date_order'].dt.strftime('%d'))['order_price'].sum()
    # print("day", day_df)

    df['year'] = df['date_order'].dt.year
    df['month'] = df['date_order'].dt.month
    df['day'] = df['date_order'].dt.day

    df_w = df.set_index(['year', 'month', 'day'])
    result = []
    if byDates == "year":
        df_ym = df_w.sum(level='year')
        for index, row in df_ym.iterrows():
            y = index
            p = row
            result.append({
                'year': y,
                'order_price': p['order_price']
            })
    elif byDates == "month":
        df_ym = df_w.sum(level=['year', 'month'])
        for index, row in df_ym.iterrows():
            y, m = index
            p = row
            result.append({
                'year': y,
                'month': m,
                'order_price': p['order_price']
            })
    else:
        df_ym = df_w.sum(level=['year', 'month', 'day'])
        for index, row in df_ym.iterrows():
            y, m, d = index
            p = row
            result.append({
                'year': y,
                'month': m,
                'day': d,
                'order_price': p['order_price']
            })

    return result

"""
https://stackoverflow.com/questions/49215096/moving-data-from-sqlalchemy-to-a-pandas-dataframe
https://strftime.org/
https://note.nkmk.me/python-pandas-time-series-multiindex/
https://www.it-swarm.dev/ja/python/python-pandas%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A6%E6%97%A5%E4%BB%98%E3%83%95%E3%82%A3%E3%83%BC%E3%83%AB%E3%83%89%E3%81%8B%E3%82%89%E6%9C%88%E3%81%94%E3%81%A8%E3%81%AB%E3%82%B0%E3%83%AB%E3%83%BC%E3%83%97%E5%8C%96%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95/833749839/

"""

def draw(datas, sel_tvalue):
    """
    To draw the graph with datas by year, month or day
    :param datas: Provided by analyzed data
    :param sel_tvalue: value selected by year, month or day
    :return: filename of graph
    """
    # its mandatory to use it for matplotlib
    # https://github.com/dghoshal-lbl/dac-man/commit/d085b9a334ee98ff4982babb11923f8c1e9eca77
    plt.switch_backend('agg')
    date = []
    order_sum = []
    if sel_tvalue == 'year':
        for data in datas:
            date.append(str(data['year']))
            order_sum.append(data['order_price'])
        # to format graph
        # https://qiita.com/senseilearning/items/7770c7f75d0909a42421
        pd_date = pd.to_datetime(date, format='%Y')
        daysFmt = mdates.DateFormatter('%Y')
    elif sel_tvalue == 'month':
        for data in datas:
            date.append(str(data['year']) + '/' + str(data['month']))
            order_sum.append(data['order_price'])
        pd_date = pd.to_datetime(date, format='%Y/%m')
        daysFmt = mdates.DateFormatter('%Y/%m')
    else:
        for data in datas:
            date.append(str(data['year']) + '/' + str(data['month']) + '/' +
                        str(data['day']))
            order_sum.append(data['order_price'])
        pd_date = pd.to_datetime(date, format='%Y/%m/%d')
        daysFmt = mdates.DateFormatter('%Y/%m/%d')

    # to secure the area of figure
    fig = plt.figure()
    # to add subplot to draw
    ax = fig.add_subplot(1, 1, 1)

    ax.bar(pd_date, order_sum, width=0.5, color=['lightblue'])
    # to format the graph
    days = mdates.DayLocator()
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(daysFmt)
    # to add "," for value
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    plt.ylabel('Total  Order($)')
    plt.xlabel(sel_tvalue)
    plt.title('Orders by ' + sel_tvalue)
    filename = 'plot.png'
    # os.path.join can track the location of the working folders
    # to save the file
    plt.savefig(os.path.join(current_app.root_path, 'static/images', filename))
    return filename