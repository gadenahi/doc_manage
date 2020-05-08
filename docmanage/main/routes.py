from flask import render_template, request, Blueprint
from docmanage.models import Report
from docmanage.sub_menu.forms import SearchForm

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    """
    To show the reports summary on the homepage
    :return: render home.html, title, reports and search_form
    """
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)
    reports = Report.query.order_by(Report.date_posted.desc()).paginate(
        page=page, per_page=20)
    return render_template('home.html', title="Market Report List",
                           reports=reports, search_form=search_form)


@main.route('/about')
def about():
    """
    To show about the reports site
    :return: render about.html, title, and search_form
    """
    search_form = SearchForm()
    return render_template('about.html', title='About',
                           search_form=search_form)
