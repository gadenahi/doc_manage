"""
This module is Report form for report website
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, TextAreaField, DateField,
                     IntegerField, RadioField)
from wtforms.validators import DataRequired, NumberRange
"""
As of Apr. 3, 2020, need to use werkzeug==0.16.0 due to the degrade of 1.0.0
"""


class ReportForm(FlaskForm):
    """
    Form for report site
    """
    title = StringField(
        'Title',
        validators=[DataRequired()],
        render_kw={"placeholder": "Title"}
    )
    date_published = DateField(
        'Published Date',
        validators=[DataRequired()],
        render_kw={"placeholder": "0000-00-00(Year-Month-Day)"}
    )
    summary = TextAreaField(
        'Summary',
        validators=[DataRequired()],
        render_kw={"placeholder": "Summary Of Report "}
    )
    table = TextAreaField(
        'Table of Content',
        validators=[DataRequired()],
        render_kw={"placeholder": "Table Of Content"}
    )
    price = IntegerField(
        'Price($)',
        validators=[NumberRange(min=100)],
        render_kw={"placeholder": "minimum 100"}
    )
    status = RadioField(
        'Status',
        choices=[("0", 'Draft'), ("1", 'Complete')]
    )
    pdf = FileField(
        'Report File',
        validators=[FileAllowed(['pdf'])]
    )
    submit = SubmitField('Post')
    # "https://wtforms.readthedocs.io/en/stable/fields/"


class OrderForm(FlaskForm):
    """
    Form for order site to send the order request without any payment
    transaction
    """
    submit = SubmitField('Send')
