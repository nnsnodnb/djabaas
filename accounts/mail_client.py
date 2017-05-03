# coding=utf-8

from django.contrib.auth.models import User
from accounts.models import UserActivateTokenModel

import random, string, os
from sendgrid.helpers.mail import *
from accounts import encryption
import sendgrid

# Register send mail
def prepare_mail_register(user, encrypt, token):
    activate_user = UserActivateTokenModel(username = user.username,
                                           token = token)
    activate_user.save()

    url = 'https://apps.nnsnodnb.moe/accounts/confirm?token=' + encrypt + '&session_id=' + token
    send_mail(u'新規登録ありがとうございます', user.username + u"""様\n\n
この度は新規登録していただきありがとうございます！\n
以下のURLよりユーザをアクティベートしてください。\n\n""" + url, user.email, 'register')

# Forget send mail
def prepare_mail_forget(user):
    password = ''.join([random.choice(string.letters + string.digits) for i in xrange(10)])
    user.set_password(password)
    user.save()
    send_mail(u'パスワード再発行', user.username + u"""様\n\n
パスワードを再発行いたしました。
ログイン後はすぐにパスワードを変更してください。\n\n
パスワード：""" + password, user.email, 'info')

# Execute sending mail
def send_mail(title, body, to, from_address):
    sg = sendgrid.SendGridAPIClient(apikey = os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(from_address + '@nnsnodnb.moe')
    subject = title
    to_email = Email(to)
    content = Content("text/plain", body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body = mail.get())
