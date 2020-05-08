from flask import (render_template, url_for, flash, redirect, request,
                   abort, Blueprint, session)
from flask_login import current_user, login_required
from docmanage import db
from docmanage.models import Report, Order
from docmanage.reports.forms import ReportForm, OrderForm
from docmanage.reports.utils import save_pdf
from docmanage.sub_menu.forms import SearchForm


reports = Blueprint('reports', __name__)


@reports.route('/report/new', methods=['GET', 'POST'])
@login_required
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
                        summary=form.summary.data,
                        table=form.table.data,
                        content=form.content.data,
                        author=form.content.data,
                        price=form.price.data,
                        status=form.status.data,
                        manager=current_user,
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
    return render_template('report.html', title=report.title, report=report,
                           search_form=search_form)


@reports.route('/report/<int:report_id>/update', methods=['GET', 'POST'])
@login_required
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
        report.summary = form.summary.data
        report.table = form.table.data
        report.content = form.content.data
        report.author = form.author.data
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
        form.summary.data = report.summary
        form.table.data = report.table
        form.content.data = report.content
        form.author.data = report.author
        form.price.data = report.price
        form.status.data = report.status
    pdf_file = url_for('static', filename='report_pdfs/' + report.pdf_file)
    return render_template('create_report.html', pdf_file=pdf_file,
                           title='Update Report', form=form,
                           legend='Update Report')


@reports.route('/report/<int:report_id>/delete', methods=['POST'])
@login_required
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
    :return:
    """
    # session['Order'] = []
    if 'Order' not in session:
        session['Order'] = []
    report = Report.query.get_or_404(report_id)
    order_list = session['Order']
    if report.status == str(1):
        if not order_list:
            order_list.append({'id': report.id, 'title': report.title,
                                'price': report.price, 'qty': 1})
            session['Order'] = order_list
            flash('The report has been added', 'success')
        else:
            data_in = False
            for data in order_list:
                if report.title in data['title']:
                    data_in = True
                    break

            if data_in is False:
                order_list.append({'id': report.id, 'title': report.title,
                                    'price': report.price, 'qty': 1})
                session['Order'] = order_list
                flash('The report has been added', 'success')
            else:
                flash('The report is already in the cart', 'success')
    else:
        flash('The report is still draft', 'success')

    return redirect(url_for('main.home'))


@reports.route('/report/<int:report_id>/remove_cart', methods=['GET', 'POST'])
def remove_cart(report_id):
    """
    To remove the report to the cart
    :param report_id:
    :return: redirect cart.html
    """

    order_list = session['Order']

    for i, data in enumerate(order_list):
        # print(i, data)
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
    :return: render cart.html, title, amount, search_form
    """
    search_form = SearchForm()
    amount = 0
    if 'Order' in session:
        cart_list = session['Order']
        for cart in cart_list:
            amount += cart['price']
        title = 'Cart'
    else:
        title = 'Cart(Empty)'

    return render_template('cart.html', title=title, amount=amount,
                           search_form=search_form)


@reports.route('/report/order', methods=['GET', 'POST'])
def new_order():
    """
    To post the order on the website
    :return: If form is submitted, redirect home.html
    At default, render order.html, title, form. legend, amount
    """
    form = OrderForm()
    cart_list = session['Order']
    amount = 0
    for cart in cart_list:
        amount += cart['price']
    # print(cart_list)
    if form.validate_on_submit():
        for cart in cart_list:
            order = Order(firstname=form.firstname.data,
                          lastname=form.lastname.data,
                          email=form.email.data,
                          report_id=cart['id'],
                          order_price=cart['price'])
            # send_email(order) # it should enable to send email
            db.session.add(order)
        db.session.commit()
        flash('Your order has been sent', 'success')
        session['Order'] = []
        return redirect(url_for('main.home'))

    return render_template('order.html', title='Order', form=form,
                           legend='Order', amount=amount)


@reports.route('/orders')
@login_required
def show_orders():
    """
    To show orders
    :return: render orders.html, title, orders, reports, amount
    """
    page = request.args.get('page', 1, type=int)
    orders = Order.query.order_by(Order.date_order.desc()).paginate(
        page=page, per_page=20)

    reports_amount = Order.query.all()
    amount = 0
    for i in reports_amount:
        amount += i.order_price

    ## internal use
    # for i in range(1, 5):
    #     orders = Order.query.get_or_404(str(i))
    #     db.session.delete(orders)
    #     db.session.commit()

    return render_template('orders.html', title='Orders', orders=orders,
                           reports=reports, amount=amount)


@reports.route('/orders/<int:report_id>')
@login_required
def show_orders_report(report_id):
    """
    To show orders by report
    :param: report_id
    :return: render orders_report.html, title, reports, report_id
    """
    page = request.args.get('page', 1, type=int)
    reports = Report.query.filter_by(id=report_id).paginate(
        page=page, per_page=20)

    return render_template('orders_report.html', title='Orders by report',
                           reports=reports, report_id=report_id)
