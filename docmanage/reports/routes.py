from docmanage import db
from docmanage.models import Report, Order, User
from docmanage.reports.forms import ReportForm, OrderForm
from docmanage.reports.utils import save_pdf, get_amount, send_email_orders
from docmanage.sub_menu.forms import SearchForm
from docmanage.sub_menu.utils import get_latest_reports
from docmanage.usersaccess.access_control import requires_access_level
from flask import (render_template, url_for, flash, redirect, request,
                   Blueprint, session)
from flask_login import current_user
import pandas as pd
from datetime import datetime


reports = Blueprint('reports', __name__)


@reports.route('/report/new', methods=['GET', 'POST'])
@requires_access_level('admin')
def new_report():
    """
    To post the new report on the website
    :return: if form is submitted, it return home.html
    At default, render create_report.html, title, form, legend
    """
    form = ReportForm()
    if form.validate_on_submit():
        report = Report(title=form.title.data,
                        date_published=form.date_published.data,
                        summary=form.summary.data.replace('\r', '<br>'),
                        table=form.table.data.replace('\r', '<br>'),
                        # https://qiita.com/gacky35/items/8498176ee80d6b6ce014
                        price=form.price.data,
                        status=form.status.data,
                        pdf_file=save_pdf(form.pdf.data)
                        )
        db.session.add(report)
        db.session.commit()
        flash('Your report has been posted', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_report.html', title='New Report',
                           form=form, legend='New Report')


@reports.route('/report/<int:report_id>')
def report(report_id):
    """
    To show the each reports
    :param report_id: unique number by report
    :return: render report.html, title, report, search_form
    """
    search_form = SearchForm()
    report = Report.query.get_or_404(report_id)
    latest_reports = get_latest_reports()
    return render_template('report.html', title=report.title, report=report,
                           search_form=search_form,
                           latest_reports=latest_reports)


@reports.route('/report/<int:report_id>/update', methods=['GET', 'POST'])
@requires_access_level('admin')
def update_report(report_id):
    """
    To update the report
    :param report_id: unique number by report
    :return: if update report submitted, redirect reports.report and report.id
    Render the create_report.html, title form
    """
    report = Report.query.get_or_404(report_id)
    form = ReportForm()
    if form.validate_on_submit():
        report.title = form.title.data
        report.date_published = form.date_published.data
        report.summary = form.summary.data.replace('\r', '<br>')
        report.table = form.table.data.replace('\r', '<br>')
        report.price = form.price.data
        report.status = form.status.data
        if form.pdf.data:
            report.pdf_file = save_pdf(form.pdf.data)
        db.session.commit()
        flash('Your report has been updated!', 'success')
        return redirect(url_for('reports.report', report_id=report_id))
    elif request.method == 'GET':
        form.title.data = report.title
        form.date_published.data = report.date_published
        form.summary.data = report.summary.replace('<br>', '\r')
        form.table.data = report.table.replace('<br>', '\r')
        form.price.data = report.price
        form.status.data = report.status
        if report.pdf_file:
            pdf_file = url_for(
                'static', filename='report_pdfs/' + report.pdf_file)
        else:
            pdf_file = None
    return render_template('create_report.html', pdf_file=pdf_file,
                           title='Update Report', form=form,
                           legend='Update Report')


@reports.route('/report/<int:report_id>/delete', methods=['POST'])
@requires_access_level('admin')
def delete_report(report_id):
    """
    To delete the report by report_id
    :param report_id: unique number by report
    :return: redirect to homepage
    """
    report = Report.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash('Your report has been deleted', 'success')
    return redirect(url_for('main.home'))


@reports.route('/report/<int:report_id>/add_cart', methods=['GET', 'POST'])
def add_cart(report_id):
    """
    To add the report to the cart
    :param report_id:
    :return: redirect to homepage
    """
    if current_user.is_authenticated:
        if 'Order' not in session:
            session['Order'] = []
        report = Report.query.get_or_404(report_id)
        order_list = session['Order']
        if report.status == str(1):
            data_in = False
            for data in order_list:
                if report.title in data['title']:
                    data_in = True
                    break

            if not order_list or data_in is False:
                order_list.append({'id': report.id, 'title': report.title,
                                    'order_price': report.price, 'qty': 1})
                session['Order'] = order_list
                flash('The report has been added', 'success')
            else:
                flash('The report is already in the cart', 'success')
        else:
            flash('The report is still draft', 'success')

        return redirect(url_for('main.home'))
    else:
        flash('Please login before adding to the cart', 'success')
        return redirect(url_for('users.login'))


@reports.route('/report/<int:report_id>/remove_cart', methods=['GET', 'POST'])
def remove_cart(report_id):
    """
    To remove the report to the cart
    :param report_id:
    :return: redirect cart.html
    """
    order_list = session['Order']
    for i, data in enumerate(order_list):
        if report_id == data['id']:
            order_list.pop(i)
            break
    session['Order'] = order_list
    flash('The report has been removed', 'success')
    return redirect(url_for('reports.show_cart'))


@reports.route('/report/cart')
def show_cart():
    """
    To show cart
    :return: render cart.html, title, amount, search_form, latest_reports
    """
    if current_user.is_authenticated:
        summary = 0
        search_form = SearchForm()
        if 'Order' in session and len(session['Order']) != 0:
            cart_list = session['Order']
            summary = get_amount(cart_list, 'session')
            title = 'Cart'
        else:
            title = 'Cart(Empty)'
        latest_reports = get_latest_reports()
        return render_template('cart.html', title=title, summary=summary,
                               search_form=search_form,
                               latest_reports=latest_reports)
    else:
        flash('Please login before proceeding the payment', 'success')
        return redirect(url_for('users.login'))


@reports.route('/report/order', methods=['GET', 'POST'])
def new_order():
    """
    To post the order on the website
    :return: If form is submitted, redirect home.html
    At default, render order.html, title, form. legend, amount
    """
    form = OrderForm()
    cart_list = session['Order']
    summary = get_amount(cart_list, "session")
    if form.validate_on_submit():
        for cart in cart_list:
            order = Order(user_id=current_user.id,
                          report_id=cart['id'],
                          order_price=cart['order_price'],
                          # date_order=datetime.utcnow() # debug purpose
                          )
            db.session.add(order)
        db.session.commit()
        # it should enable to send email
        send_email_orders(current_user, cart_list, summary=summary)
        flash('Your order has been sent', 'success')
        session['Order'] = []
        return redirect(url_for('main.home'))
    return render_template('order.html', title='Order', form=form,
                           summary=summary)


@reports.route('/orders')
@requires_access_level('admin')
def show_orders():
    """
    To show orders
    :return:render orders.html, title, orders, reports, summary, latest_reports
    """
    page = request.args.get('page', 1, type=int)
    orders = Order.query.order_by(Order.date_order.desc()).paginate(
        page=page, per_page=100)
    orders_amount = Order.query.all()
    if len(orders_amount) != 0:
        summary = get_amount(orders_amount, "order")
    else:
        summary = None
    latest_reports = get_latest_reports()
    return render_template('orders.html', title='Orders', orders=orders,
                           reports=reports, summary=summary,
                           latest_reports=latest_reports)


@reports.route('/orders/report/<int:report_id>')
@requires_access_level('admin')
def show_orders_report(report_id):
    """
    To show orders by report
    :param: report_id
    :return: render orders_report.html, title, orders, report, summary
    """
    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(report_id=report_id).paginate(
        page=page, per_page=100)
    orders_amount = Order.query.filter_by(report_id=report_id).all()
    report = Report.query.filter_by(id=report_id).first()
    summary = get_amount(orders_amount, "order")
    return render_template('orders_report.html', title='Orders by report',
                           orders=orders, report=report, summary=summary)


@reports.route('/orders/user/<int:user_id>')
@requires_access_level('admin')
def show_orders_user(user_id):
    """
    To show orders by user
    :param: email
    :return: render orders_user.html, title, orders, user, summary
    """
    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(user_id=user_id).paginate(
        page=page, per_page=100)
    orders_amount = Order.query.filter_by(user_id=user_id).all()
    summary = get_amount(orders_amount, "order")
    user = User.query.filter_by(id=user_id).first()
    return render_template('orders_user.html', title='Orders by user',
                           orders=orders, user=user, summary=summary)


@reports.route('/customers')
@requires_access_level('admin')
def show_customers():
    """
    To show customers
    :param:
    :return: render customers.html, title, orders, user, summary
    """
    page = request.args.get('page', 1, type=int)
    customers = User.query.order_by(User.firstname.desc()).paginate(
        page=page, per_page=100)
    return render_template('customers.html', title='Customers',
                           customers=customers)


@reports.route('/upload', methods=['GET', 'POST'])
@requires_access_level('admin')
def upload_list():
    if request.method == 'POST':
        f = request.files['send_file']
        data_xls = pd.read_excel(f)
        for index, data in data_xls.iterrows():
            checkReport = Report.query.filter_by(title=data["title"]).first()
            if not checkReport:
                report = Report(title=data["title"],
                                date_published=data["date_published"],
                                summary=data["summary"].replace('\n', '<br>'),
                                table=data["table"].replace('\n', '<br>'),
                                price=data["price"],
                                status=data["status"]
                                )
                db.session.add(report)
            else:
                flash('Same report name is already exist', 'success')
                return redirect(url_for('reports.upload_list'))
        db.session.commit()
        flash('Your list has been uploaded', 'success')
        return redirect(url_for('main.home'))
    excelformat = url_for(
        'static', filename='report_format/' + "report_format.xlsx")
    return render_template('upload_list.html', title='Upload Report List',
                           excelformat=excelformat)


