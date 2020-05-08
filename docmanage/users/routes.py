from docmanage import db, bcrypt
from docmanage.models import User
from docmanage.users.forms import RegistrationForm, LoginForm,\
    UpdateAccountForm, UpdatePasswordForm
from flask import render_template, url_for, redirect, request, Blueprint, flash
from flask_login import current_user, login_user, logout_user, login_required


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    """
    To register the account for new users
    :return: if authenticated, redirect to homepage.
    if registration is submitted, redirect to login page.
    At default, render registration page, title, form
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.
                                                        data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    """
    To login
    :return: if authenticated, redirected to homepage
    if login form is submitted, and url contains next, redirect to next page,
    otherwise to homepage
    At default render login.html, title
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in !', 'success')
            return redirect(next_page) if next_page else redirect(
                url_for('main.home')
            )
        else:
            flash('Login Unsuccessful')

    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    """
    To logout
    :return: redirect to homepage
    """
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """
    To update the account information
    :return: if the form is submitted, redirect to user.account, else render
    account.html, title, form
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html', title='Account', form=form)


@users.route('/account/<string:username>/update_password',
             methods=['GET', 'POST'])
@login_required
def update_password(username):
    """
    To update password with authenticated user
    :param username: current login user
    :return: if form is submitted, redirect to users.account
    At default, render update_password.html, title, form
    """
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.oldpassword.data):
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated', 'success')
            return redirect(url_for('users.account'))

    return render_template('update_password.html',
                           title='Update Password', form=form)









