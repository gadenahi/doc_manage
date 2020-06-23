"""
This module is setting for SQL server
"""

import os


class Config:
    """
    Setting for SQL and mail server
    """
    # .bash-profile
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Didnt user for Flask-user
    # roles_required default parameters
    # MAIL_DEFAULT_SENDER = '"Sender" < noreply@test.com >'
    # USER_APP_NAME = "Flask-User Hello"  # Shown in and email templates and page footers
    # USER_ENABLE_EMAIL = False  # Disable email authentication
    # USER_ENABLE_USERNAME = True  # Enable username authentication
    # USER_REQUIRE_RETYPE_PASSWORD = False  # Simplify register form
    # USER_UNAUTHENTICATED_ENDPOINT = "users.login"
    # https://flask-user.readthedocs.io/en/latest/authorization.html
    # https://flask-user.readthedocs.io/en/v0.6/api.html
    # https://github.com/lingthio/Flask-User/blob/master/flask_user/user_manager__views.py
    # https://stackoverflow.com/questions/43201102/flask-customising-flask-user-login
