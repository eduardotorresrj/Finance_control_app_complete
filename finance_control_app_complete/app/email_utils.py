from flask_mail import Message
from app import mail
from flask import render_template
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(app, subject, recipients, template, **kwargs):
    msg = Message(subject, recipients=[recipients])
    msg.html = render_template(template, **kwargs)
    Thread(target=send_async_email, args=(app, msg)).start()
