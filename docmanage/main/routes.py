from flask import Blueprint, render_template, request

from docmanage.models import Report
from docmanage.sub_menu.forms import SearchForm
from docmanage.sub_menu.utils import get_latest_reports


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    """
    To show the reports summary on the homepage
    :return: render home.html, title, reports, search_form, latest_reports
    """
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)
    reports = Report.query.order_by(Report.date_posted.desc()).paginate(
        page=page, per_page=100)
    latest_reports = get_latest_reports()
    return render_template('home.html', title="Market Report List",
                           reports=reports, search_form=search_form,
                           latest_reports=latest_reports)


@main.route('/about')
def about():
    """
    To show about the reports site
    :return: render about.html, title, search_form and latest_reports
    """
    search_form = SearchForm()
    latest_reports = get_latest_reports()
    return render_template('about.html', title='About',
                           search_form=search_form,
                           latest_reports=latest_reports)
