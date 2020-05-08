from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    """
    Form for search site
    """
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('GO')
