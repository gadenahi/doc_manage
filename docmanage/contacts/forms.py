from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ContactForm(FlaskForm):
    """
    Form for contact site
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
    subject = StringField(
        'Subject',
        validators=[DataRequired(), Length(min=2, max=30)],
        render_kw={"placeholder": "What's is your purpose"}
    )
    message = StringField(
        'Message',
        validators=[DataRequired(), Length(min=2, max=30)],
        render_kw={"placeholder": "Please describe the detail"}
    )
    submit = SubmitField('Send')

