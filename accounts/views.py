# coding=utf-8

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template.context_processors import csrf
import urllib, random, string

def register(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password_confirm']:
            user = User.objects.create_user(username = request.POST['username'],
                                            email = urllib.unquote(request.POST['email']),
                                            password = request.POST['password'])
            try:
                user.save()
                execute_login('push:index', request.POST['username'], request.POST['password'])
            except Exception as e:
                return HttpResponse(e)
        else:
            c = {}
            c.update(csrf(request))
            return render(request, 'accounts/register.html', c)
    else:
        c = {}
        c.update(csrf(request))
        return render(request, 'accounts/register.html', c)

def forget(request):
    if request.method == 'POST':
        if request.POST['username'] != '':
            user = User.objects.get(username = request.POST['username'])
            prepare_mail(user)
        elif request.POST['email'] != '':
            user = User.objects.get(email = request.POST['email'])
            prepare_mail(user)
        else:
            return redirect('accounts:forget')

        return HttpResponse('ご登録のメールアドレスに仮パスワードを送信しました')
    else:
        c = {}
        c.update(csrf(request))
        return render(request, 'accounts/forget.html', c)

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
            execute_login('push:settings', user.username, new)
    else:
        return HttpResponse('Access Denied', status = 403)

def prepare_mail(user):
    password = ''.join([random.choice(string.letters + string.digits) for i in xrange(10)])
    user.set_password(password)
    user.save()
    send_mail(u'パスワード再発行', user.username + u"""様\n\n
パスワードを再発行いたしました。
ログイン後はすぐにパスワードを変更してください。\n\n
パスワード：""" + password, user.email)

def send_mail(title, body, to):
    try:
        EmailMessage(title, body, to = [to]).send()
        return HttpResponse('Send your register email')
    except Exception as e:
        return HttpResponse(e)

def execute_login(redirect_url, username, password):
    login_user = authenticate(username = username, password = password)
    if login_user is not None:
        if login_user.is_active:
            login(request, login_user)
            return redirect(redirect_url)
        else:
            return HttpResponse('Login Error', status = 401)
    else:
        return HttpResponse('Login Error', status = 401)
