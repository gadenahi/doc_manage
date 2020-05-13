import os
import secrets
from flask import current_app, request
import pandas as pd


def save_pdf(form_pdf):
    """
    To save pdf with unique name
    :param form_pdf: form pdf
    :return: name of pdf
    """
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
    return df['order_price'].sum()
