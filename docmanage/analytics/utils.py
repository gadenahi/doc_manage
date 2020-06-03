import os
from docmanage.models import Order
from flask import current_app
import calendar
import pandas as pd
import matplotlib.pyplot as plt


def analyze_data_draw(bydates):
    """
    To summarize the data for table by sum, mean and count, and create and save
    graph
    :param bydates: select options by year, month, or day
    :return: array for table datas and filename of graph
    """
    order_query = Order.query.all()
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


"""
    start = datetime(year=int(year), month=int(start_month), day=1)
    # To get the last date by month automatically
    last_day = calendar.monthrange(int(year), int(start_month))[1]
    # To set the end date for the filter
    end = datetime(year=int(year), month=int(end_month), day=int(last_day))
    posts = Post.query.filter(Post.date_posted <= end)\
        .filter(Post.date_posted >= start)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
"""