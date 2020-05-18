from flask import render_template, Blueprint, request, url_for
from docmanage.analytics.utils import analyze_data_draw
from flask import current_app
import os


analytics = Blueprint('analytics', __name__)


@analytics.route('/analytics', methods=['GET', 'POST'])
def analize():
    """
    To analyze the orders data
    :return: render analytics.html, title, byDates, sel_tvalue,
    resAnalyzeDatas, plt_name, and legend
    """
    byDates = ['year', 'month', 'day']
    # To get the value of select
    byDate = request.form.get("byDate")
    if byDate is None:
        sel_tvalue = 'year'
    else:
        sel_tvalue= byDate
    # To get the analized data by byDate and plt_name
    resAnalyzeDatas, plt_name = analyze_data_draw(sel_tvalue)
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
