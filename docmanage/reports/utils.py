import os
import secrets
from flask import current_app, request, render_template
import pandas as pd
from flask_mail import Message
from docmanage import mail
from docmanage.config import Config


def save_pdf(form_pdf):
    """
    To save pdf with unique name
    :param form_pdf: form pdf
    :return: name of pdf
    """
    if form_pdf:
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_pdf.filename)
        pdf_fn = random_hex + f_ext
        file = request.files['pdf']  # name of input on html
        file.save(os.path.join(
            current_app.root_path,
            'static/report_pdfs',
            pdf_fn)
        )
        return pdf_fn
    else:
        return

"""
https://qiita.com/5zm/items/ac8c9d1d74d012e682b4
https://stackoverflow.com/questions/44861266/flask-generate-preview-pdf-with-reportlab
"""


def get_amount(data, req):
    """
    :param data: input from session or orders
    :param req: "requested by session or orders"
    :return: sum of order_price
    """
    if req == 'session':
        df = pd.DataFrame(data)
    elif req == "order":
        df = pd.DataFrame([d.order_price for d in data],
                          columns=["order_price"])

    summary = dict()
    summary['amount'] = df['order_price'].sum()
    summary['average'] = int(df['order_price'].mean())
    summary['count'] = df['order_price'].count()

    return summary


config = Config()
config.MAIL_USERNAME


def send_email_orders(user, cart_list, summary):
    """
    To send the email with the input by contact form
    :param user: user for orders
    :param cart_list: orderslist
    :param summary: total ammount of orders
    :return: None
    """

    msg = Message('Thank you for your orders of Market Report',
                  sender='noreply@demo.com',
                  recipients=[user.email, config.MAIL_USERNAME])
    msg.html = render_template('order_email.html', user=user,
                             cart_list=cart_list, summary=summary)

    # https://stackoverflow.com/questions/49363657/using-flask-mail-to-send-the-rendered-form

    mail.send(msg)

