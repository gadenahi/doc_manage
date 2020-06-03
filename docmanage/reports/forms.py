"""
This module is Report form for report website
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, TextAreaField, DateField,
                     IntegerField, RadioField)
from wtforms.validators import DataRequired, NumberRange, Length, Email
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
        render_kw={"placeholder": "Report title"}
    )
    date_published = DateField(
        'Published Date',
        validators=[DataRequired()],
        render_kw={"placeholder": "0000-00-00(year-month-day)"}
    )
    summary = TextAreaField(
        'Summary',
        validators=[DataRequired()],
        render_kw={"placeholder": "summary of report "}
    )
    table = TextAreaField(
        'Table of Content',
        validators=[DataRequired()],
        render_kw={"placeholder": "e.g. 1. The purpose of report"}
    )
    content = TextAreaField(
        'Content',
        validators=[DataRequired()],
        render_kw={"placeholder": "Describe the detail"}
    )
    author = TextAreaField(
        'Author',
        validators=[DataRequired()],
        render_kw={"placeholder": "Last name First name"}
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
    firstname = StringField(
        'Firstname',
        validators=[DataRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": "Enter your first name"}
    )
    lastname = StringField(
        'Lastname',
        validators=[DataRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": "Enter your last name"}
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField('Send')
