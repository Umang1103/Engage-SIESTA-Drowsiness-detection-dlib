from flask_mail import Message
from flask import current_app
from flask import url_for
from PIL import Image
from flaskapp import mail
from twilio.rest import Client
from flaskapp.models import User
from flask_login import current_user
import secrets
import os

account_sid = 'AC8638d78e74311ca9f871bec34dc25343'
auth_token = '538ac68fd8a534b8bc17bf8484204c61'

client = Client(account_sid, auth_token)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images/', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.body = f'''
    Click on the following link to reset your password:
    {url_for('users.reset_token', token=token, _external=True)}

    If you did not make this request, then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)


def alert_mail():
    user = User.query.get(id=current_user.id)
    message = client.messages.create(
        from_='+19362263389',
        body=f'''
    !!! SLEEP ALERT !!!

    You're about to Sleep. Either take a nap or get yourself a coffee.
    ''',
        to=user.contact
    )
    print(f'To: {user.contact} \n Content: {message}')
