# coding=utf-8

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
import urllib, random, string, os
from accounts.models import UserActivateTokenModel
from accounts import encryption, mail_client

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
                    mail_client.prepare_mail_register(user, str(encrypt_pass), tail_word)
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
            mail_client.prepare_mail_forget(user)
        elif request.POST['email'] != '':
            user = User.objects.get(email = request.POST['email'])
            mail_client.prepare_mail_forget(user)
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
                return render(request, 'push/top.html', {"is_first": True})
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
