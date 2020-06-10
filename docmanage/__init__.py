"""
This module is initiate the application and register the routes and handlers to
blueprint
"""
from docmanage.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_msearch import Search
from flask_mail import Mail
from flask_admin import Admin


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'  # setting for login route
login_manager.login_message_category = 'info'
mail = Mail()


def admin_control(app):
    from docmanage.admincc.admincontrol import MyAdminIndexView, MyModelView
    from docmanage.models import User, Report, Order
    adminCC = Admin(app, index_view=MyAdminIndexView())
    adminCC.add_view(MyModelView(User, db.session))
    adminCC.add_view(MyModelView(Report, db.session))
    adminCC.add_view(MyModelView(Order, db.session))


def create_app(config_class=Config):
    """
    Initiate application and register the routes and handlers to blueprint
    :param config_class: setting for sql
    :return: application initiate and blueprint mapping
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    search = Search()
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    search.init_app(app)
    mail.init_app(app)

    from docmanage.main.routes import main
    from docmanage.users.routes import users
    from docmanage.reports.routes import reports
    from docmanage.sub_menu.routes import sub_menu
    from docmanage.contacts.routes import contacts
    from docmanage.errors.handlers import errors
    from docmanage.analytics.routes import analytics

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(reports)
    app.register_blueprint(sub_menu)
    app.register_blueprint(contacts)
    app.register_blueprint(errors)
    app.register_blueprint(analytics)

    admin_control(app)

    return app


