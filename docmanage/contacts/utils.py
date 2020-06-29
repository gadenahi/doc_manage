from flask_mail import Message

from docmanage import mail
from docmanage.config import Config

config = Config()
config.MAIL_USERNAME


def send_email(contact):
    """
    To send the email with the input by contact form
    :param contact: input from contact form
    :return: None
    """
    msg = Message('Thank you for your contact from Market Report',
                  sender='noreply@demo.com',
                  recipients=[contact.email, config.MAIL_USERNAME])
    msg.body = """
    From: %s %s <%s>
    Object: %s
    Message: %s
    """ % (contact.firstname, contact.lastname, contact.email,
           contact.subject, contact.message)
    mail.send(msg)
