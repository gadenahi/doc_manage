from flask import Blueprint, render_template, request, url_for
from flask import current_app
import os

from docmanage.analytics.utils import (analyze_data_draw, cal_days, cal_months,
                                       cal_years)
from docmanage.usersaccess.access_control import requires_access_level


analytics = Blueprint('analytics', __name__)


@analytics.route('/analytics', methods=['GET', 'POST'])
@requires_access_level('admin')
def analize():
    """
    To analyze the orders data
    :return: render analytics.html, title, byDates, sel_tvalue,
    resAnalyzeDatas, plt_name, and legend
    """
    byDates = ['year', 'month', 'day']
    # To get the value of select
    sel_tvalue = request.form.get("byDate")
    if sel_tvalue is None:
        sel_tvalue = 'year'

    # didn't use
    # To get the select byDates by get_select_data.js
    # sel_tvalue = request.args.get('filter_date', None)
    # if sel_tvalue is None:
    #     sel_tvalue = 'year'

    # to get data for certain duration by input sel_tvalue
    if sel_tvalue == 'day':
        order_query = cal_days()
    elif sel_tvalue == 'month':
        order_query = cal_months()
    else:
        order_query = cal_years()
    # To get the analized data by byDate and plt_name
    if len(order_query) != 0:
        resAnalyzeDatas, plt_name = analyze_data_draw(sel_tvalue, order_query)
    else:
        resAnalyzeDatas, plt_name = None, None
    legend = 'Orders by ' + sel_tvalue

    return render_template('analytics.html', title='Orders Analytics',
                           byDates=byDates, sel_tvalue=sel_tvalue,
                           resAnalyzeDatas=resAnalyzeDatas, plt_name=plt_name,
                           legend=legend)

"""
To avoid the cache issues for image for analized dat
https://aroundthedistance.hatenadiary.jp/entry/2015/01/28/101902
"""


@analytics.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(current_app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
