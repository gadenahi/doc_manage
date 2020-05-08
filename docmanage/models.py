"""
This module is models for User and Report
"""
from datetime import datetime
from docmanage import db, login_manager
from flask_login import UserMixin


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
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    reports = db.relationship('Report', backref='manager', lazy=True)

    def __repr__(self):
        """
        for the debug purpose by shell script
        :return:username and email
        """
        return "User('{}', '{}')".format(self.username, self.email)


class Report(db.Model):
    """
    Report models for report information for report site
    """
    __searchable__ = ['title', 'summary', 'table', 'author', 'status']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    date_published = db.Column(db.Date, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    table = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    pdf_file = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order = db.relationship('Order', backref='report', lazy=True)

    def __repr__(self):
        """
        for the debug purpose by shell script
        :return: title, date_published and author
        """
        return "Report(id:'{}', title:'{}', status:'{}', price:'{}'," \
                "order:'{}')".format(
            self.id, self.title, self.status, self.price, self.order)


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
        :return:firstname, username and email
        """
        return "Contact('{}', '{}', '{}')".format(self.firstname, self.lastname,
                                         self.email)


class Order(db.Model):
    """
    User models for Order information
    """
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'),
                          nullable=False)
    order_price = db.Column(db.Integer, nullable=False)
    date_order = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __repr__(self):
        """
        for the debug purpose by shell script
        :return:firstname, username and email
        """
        return "Order(id:'{}', firstname:'{}', lastname:'{}', email:'{}'," \
               "report_id:'{}', order_price:'{}', date_order:'{}')"\
            .format(self.id, self.firstname, self.lastname, self.email,
                    self.report_id, self.order_price, self.date_order)


class OrderDetail(db.Model):
    """
    OrderDetail for Order and customer information
    """
    id = db.Column(db.Integer, primary_key=True)

