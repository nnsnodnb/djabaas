# coding=utf-8

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template.context_processors import csrf
import urllib, random, string, os, sendgrid
from sendgrid.helpers.mail import *
from accounts.models import UserActivateTokenModel
import encryption

def register(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password_confirm']:
            try:
                user = User.objects.create_user(username = request.POST['username'],
                                                email = urllib.unquote(request.POST['email']),
                                                password = request.POST['password'],
                                                is_active = False)
                user.save()
            except Exception as e:
                return render(request, 'accounts/register.html', {'error': 'unique_error'})

            login_user = authenticate(username = request.POST['username'],
                                      password = request.POST['password'])
            if login_user is not None:
                if login_user.is_active:
                    login(request, login_user)
                    return redirect('push:index')
                else:
                    tail_word = ''.join([random.choice(string.letters + string.digits) for i in xrange(5)])
                    encrypt_pass = encryption.execute_encryption(True, request.POST['password'])
                    prepare_mail_register(user, str(encrypt_pass), tail_word)
                    return HttpResponse('入力されたメールアドレスにメールを送信しました。ご確認お願いします。')
            else:
                return redirect('accounts:login')
        else:
            return render(request, 'accounts/register.html', {'error': 'password'})
    else:
        return render(request, 'accounts/register.html')

def forget(request):
    if request.method == 'POST':
        if request.POST['username'] != '':
            user = User.objects.get(username = request.POST['username'])
            prepare_mail_forget(user)
        elif request.POST['email'] != '':
            user = User.objects.get(email = request.POST['email'])
            prepare_mail_forget(user)
        else:
            return redirect('accounts:forget')

        return HttpResponse('ご登録のメールアドレスに仮パスワードを送信しました')
    else:
        return render(request, 'accounts/forget.html')

@login_required(login_url = '/accounts/login/')
def change_password(request):
    if request.method == 'POST':
        old = request.POST['old_password']
        new = request.POST['new_password']
        confirm = request.POST['confirm']
        user = User.objects.get(username = request.user.username)
        if user.check_password(old) and new == confirm:
            user.set_password(new)
            user.save()
            logout(request)
            login_user = authenticate(username = user.username, password = new)
            if login_user is not None:
                if login_user.is_active:
                    login(request, login_user)
                    return redirect('push:settings')
                else:
                    return HttpResponse('Login Error', status = 401)
            else:
                return HttpResponse('Login Error', status = 401)
        else:
            return HttpResponse('Login Error', status = 401)
    else:
        return HttpResponse('Access Denied', status = 403)

def confirm(request):
    if request.method == 'GET':
        encrypt_pass = request.GET['token']
        session_id = request.GET['session_id']
        activate_user = UserActivateTokenModel.objects.filter(token = request.GET['session_id'])[0]

        decrypted_pass = encryption.execute_encryption(False, encrypt_pass)

        activate_user.is_user = True
        activate_user.delete()

        user = User.objects.get(username = activate_user.username)
        user.is_active = True
        user.save()
        login_user = authenticate(username = user.username, password = decrypted_pass)
        if login_user is not None:
            if login_user.is_active:
                login(request, login_user)
                return redirect('push:index')
            else:
                return HttpResponse('Login Error', status = 401)
        else:
            return HttpResponse('Login Error', status = 401)
    else:
        return redirect('accounts:login')

@login_required(login_url = '/accounts/login/')
def delete_user(request):
    if request.method == 'POST':
        password = request.POST['password']
        user = User.objects.get(username = request.user.username)
        if user.check_password(password):
            user.is_active = False
            try:
                user.save()
            except Exception as e:
                return HttpResponse(e, status = 500)
            return redirect('accounts:complete_delete')
        else:
            return render(request, 'push/settings.html', {'result': 'pass_miss'})
    else:
        return HttpResponse('Not allowed method', status = 405)

def complete_delete(request):
    return render(request, 'accounts/delete.html')

def prepare_mail_register(user, encrypt, token):
    activate_user = UserActivateTokenModel(username = user.username,
                                           token = token)
    activate_user.save()

    url = 'https://apps.nnsnodnb.moe/accounts/confirm?token=' + encrypt + '&session_id=' + token
    send_mail(u'新規登録ありがとうございます', user.username + u"""様\n\n
この度は新規登録していただきありがとうございます！\n
以下のURLよりユーザをアクティベートしてください。\n\n""" + url, user.email, 'register')

def prepare_mail_forget(user):
    password = ''.join([random.choice(string.letters + string.digits) for i in xrange(10)])
    user.set_password(password)
    user.save()
    send_mail(u'パスワード再発行', user.username + u"""様\n\n
パスワードを再発行いたしました。
ログイン後はすぐにパスワードを変更してください。\n\n
パスワード：""" + password, user.email, 'info')

def send_mail(title, body, to, from_address):
    try:
        sg = sendgrid.SendGridAPIClient(apikey = os.environ.get('SENDGRID_API_KEY'))
        from_email = Email(from_address + '@nnsnodnb.moe')
        subject = title
        to_email = Email(to)
        content = Content("text/plain", body)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body = mail.get())
        return HttpResponse('Send your register email', status = 200)
    except Exception as e:
        return HttpResponse(e, status = 500)

def execute_login(redirect_url, username, password, request):
    login_user = authenticate(username = username, password = password)
    if login_user is not None:
        if login_user.is_active:
            login(request, login_user)
            return redirect(redirect_url)
        else:
            return HttpResponse('Login Error', status = 401)
    else:
        return HttpResponse('Login Error', status = 401)
