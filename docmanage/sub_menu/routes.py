from flask import render_template, Blueprint, request
from docmanage.models import Report
from docmanage.sub_menu.forms import SearchForm


sub_menu = Blueprint('sub_menu', __name__)


@sub_menu.route('/search', methods=['GET'])
def search():
    """
    To search the report info with the condition
    :return: home.html, title, reports, search_form and q
    """
    q = request.args.get('search', '')  # name attribute on HTML
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)
    results = Report.query.msearch(q).paginate(page=page, per_page=100)
    return render_template('home.html', title="result:" + q,
                           reports=results, search_form=search_form, q=q)

"""
https://github.com/honmaple/flask-msearch
https://stackoverflow.com/questions/52914082/flask-format-site-url-to-display-search-query
"""
