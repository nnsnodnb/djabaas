# coding=utf-8

from django.contrib.auth import authenticate, login
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
                return HttpResponse(e)
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
        print('GET')
        c = {}
        c.update(csrf(request))
        return render_to_response('accounts/forget.html', c)

@login_required(login_url = '/accounts/login/')
def change_pass(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        new_confirm = request.POST['new_confirm']
        user = User.objects.get(username = request.user.username)
        if user.password == old_password and new_password == new_confirm:
            print(user.password)
            user.set_password(new_password)
            user.save()
            return redirect('push:index')
        else:
            return redirect('push:settings')
    else:
        return redirect('push:settings')

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
