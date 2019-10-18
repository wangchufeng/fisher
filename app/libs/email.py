from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_email(to, subject, template, **kwargs):
    msg = Message('[鱼书]' + ' ' + subject, sender=current_app.config['MAIL_USERNAME'], body='Test',
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    # 由于开启了一个新的线程，由于Flask线程隔离的作用，需要传入一个真实的核心对象app
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email(app, msg))
    thr.start()
    # mail.send(msg)

