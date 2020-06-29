"""
This module is models for User and Report
"""
from datetime import datetime
from flask_login import UserMixin
from docmanage import db, login_manager


@login_manager.user_loader
def loader_user(user_id):
    """
    To get the user information when the login.
    :param user_id: login user_id
    :return: login user_id
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    User models for user information
    """
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(30), nullable=False)
    jobtitle = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'),
                           nullable=False)
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('by_roles', lazy='dynamic'))
    orders = db.relationship('Order', backref='orders', lazy=True)

    def is_admin(self):
        return self.roles[0].rolename == 'admin'

    def country_name(self, country_id):
        country = Country.query.filter_by(id=country_id).first()
        return country.countryname

    def __repr__(self):
        """
        for the debug purpose by shell script
        :return:id, firstname, lastname, company, jobtitle, email, county_id,
        role_id
        """
        return "User(id:'{}', firstname:'{}', lastname:'{}', company:'{}', " \
               "jobtitle:'{}', email:'{}', country_id:'{}', roles'{}')"\
            .format(self.id, self.firstname, self.lastname, self.company,
                    self.jobtitle, self.email, self.country_id, self.roles)


class Role(db.Model):
    """
    Role for User, user or admin
    """
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(50), unique=True)
    users = db.relationship('User', secondary='user_roles',
                            backref=db.backref('by_users', lazy='dynamic'))

    def __repr__(self):
        """
        for the debug purpose by shell script
        :return:id, rolename and users
        """
        return "Role(id:'{}', rolename:'{}', users:'{}')".format(
            self.id, self.rolename, self.users)


class UserRoles(db.Model):
    """
    Role for User, user or admin
    """
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(),
                        db.ForeignKey('role.id', ondelete='CASCADE'))

    def __repr__(self):
        """
        for the debug purpose by shell script
        :return:id, rolename and users
        """
        return "Role(id:'{}', user_id:'{}', role_id:'{}')".format(
            self.id, self.user_id, self.role_id)


class Country(db.Model):
    """
    Country for User
    """
    id = db.Column(db.Integer, primary_key=True)
    countryname = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='user_country', lazy=True)

    def __repr__(self):
        """
        for the debug purpose by shell script
        :return:id, countryname and users
        """
        return "Country(id:'{}', countryname:'{}', users:'{}')".format(
            self.id, self.countryname, self.users)


class Report(db.Model):
    """
    Report models for report information for report site
    """
    __searchable__ = ['title', 'summary', 'table', 'status']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    date_published = db.Column(db.Date, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    table = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    pdf_file = db.Column(db.String(30), nullable=True)
    orders = db.relationship('Order', backref='buyer', lazy=True)

    def __repr__(self):
        """
        for the debug purpose by shell script
        :return: id, title, date_published, price, status, orders
        """
        return "Report(id:'{}', title:'{}', date_published: '{}', price:'{}'" \
               ", , status:'{}', orders:'{}')"\
            .format(self.id, self.title, self.date_published, self.price,
                    self.status, self.orders)


class Contact(db.Model):
    """
    User models for contact information
    """
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(30), nullable=False)
    message = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        """
        for the debug purpose by shell script
        :return:id, firstname, lastname and email
        """
        return "Contact(id:'{}', firstname:'{}', lastname:'{}', email:'{}')"\
            .format(self.id, self.firstname, self.lastname, self.email)


class Order(db.Model):
    """
    User models for Order information
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'),
                          nullable=False)
    order_price = db.Column(db.Integer, nullable=False)
    date_order = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def get_users(self, user_id):
        return User.query.filter_by(id=user_id)

    def __repr__(self):
        """
        for the debug purpose by shell script
        :return:id, user_id, report_id, order_price, date_order
        """
        return "Order(id:'{}', user_id:'{}',report_id:'{}', order_price:'{}',"\
               "date_order:'{}')".format(self.id, self.user_id, self.report_id,
                                         self.order_price, self.date_order)
