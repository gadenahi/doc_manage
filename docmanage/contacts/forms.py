from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    """
    Form for contact site
    """
    firstname = StringField(
        'First Name',
        validators=[DataRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": "First Name"}
    )
    lastname = StringField(
        'Last Name',
        validators=[DataRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": "Last Name"}
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw = {"placeholder": "Email"}
    )
    subject = StringField(
        'Subject',
        validators=[DataRequired(), Length(min=2, max=30)],
        render_kw={"placeholder": "Your Subject"}
    )
    message = TextAreaField(
        'Message',
        validators=[DataRequired(), Length(min=2, max=200)],
        render_kw={"placeholder": "Your Message"}
    )
    submit = SubmitField('Send')

