from flask import Blueprint, flash, redirect, render_template, url_for

from docmanage import db
from docmanage.contacts.forms import ContactForm
from docmanage.contacts.utils import send_email
from docmanage.models import Contact


contacts = Blueprint('contacts', __name__)


@contacts.route('/contacts', methods=['GET', 'POST'])
def new_contact():
    """
    To post the new contact on the website
    :return: if form is submitted, return home.html.
    At default, render contacts.html, title, form, legend
    """
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(firstname=form.firstname.data,
                          lastname=form.lastname.data,
                          email=form.email.data,
                          subject=form.subject.data,
                          message=form.subject.data)
        send_email(contact)
        db.session.add(contact)
        db.session.commit()
        flash('Your contact has been sent', 'success')
        return redirect(url_for('main.home'))

    return render_template('contacts.html', title='Contact', form=form,
                           legend='Contact')
