from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (DataRequired, Length, Email,
                                EqualTo, ValidationError)
from flask_login import current_user
from docmanage.models import User


class RegistrationForm(FlaskForm):
    """
    Form for user site
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """
        To validate the username if it is already exist
        :param username: username on the form
        :return: if username submitted form is already exist, return error
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username is used already')

    def validate_email(self, email):
        """
        To validate the email if it is already exist
        :param email: email on the form
        :return: if email submitted form is already exist, return error
        """
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('The email is used already')


class LoginForm(FlaskForm):
    """
    Form for login site
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class UpdateAccountForm(FlaskForm):
    """
    Form for update account
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        """
        To validate the username if it is already exist
        :param username: username on the form
        :return: if username submitted form is already exist, return error
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The username is used already')

    def validate_email(self, email):
        """
        To validate the email if it is already exist
        :param email: email on the form
        :return: if email submitted form is already exist, return error
        """
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('The email is used already')


class UpdatePasswordForm(FlaskForm):
    """
    Form for update password
    """
    oldpassword = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Update Password')