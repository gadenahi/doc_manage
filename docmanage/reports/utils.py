import os
import secrets
from flask import current_app, request


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

