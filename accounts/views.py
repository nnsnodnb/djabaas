# coding=utf-8

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template.context_processors import csrf
import urllib, random, string

def register(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password_confirm']:
            user = User.objects.create_user(request.POST['username'],
                                            urllib.unquote(request.POST['email']),
                                            request.POST['password'])
            try:
                user.save()
                login_user = authenticate(username = request.POST['username'],
                                          password = request.POST['password'])
                if login_user is not None:
                    if login_user.is_active:
                        login(request, login_user)
                        return redirect('push:index')
                    else:
                        return HttpResponse('Login Error')
                else:
                    return HttpResponse('Login Error')
            except Exception as e:
                raise
        else:
            c = {}
            c.update(csrf(request))
            return render_to_response('accounts/register.html', c)
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('accounts/register.html', c)

def forget(request):
    if request.method == 'POST':
        if request.POST.has_key('username'):
            user = User.objects.get(username = request.POST['username'])

            password = ''.join([random.choice(string.letters + string.digits) for i in xrange(10)])
            user.set_password(password)
            user.save()
            send_mail(u'パスワード再発行', user.username + u"""様\n\n
パスワードを再発行いたしました。
ログイン後はすぐにパスワードを変更してください。\n\n
パスワード：""" + password, user.email)
        return HttpResponse('ご登録のメールアドレスに仮パスワードを送信しました')
    else:
        print('GET')
        c = {}
        c.update(csrf(request))
        return render_to_response('accounts/forget.html', c)

def send_mail(title, body, to):
    try:
        EmailMessage(title, body, to = [to]).send()
        return HttpResponse('Send your register email')
    except Exception as e:
        raise
