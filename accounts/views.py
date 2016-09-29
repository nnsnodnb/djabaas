from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template.context_processors import csrf
import urllib

def register(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password_confirm']:
            user = User.objects.create_user(request.POST['username'],
                                            urllib.unquote(request.POST['email']),
                                            request.POST['password'])
            user.save()
            login_user = authenticate(username = request.POST['username'], password = request.POST['password'])
            if login_user is not None:
                if login_user.is_active:
                    login(request, login_user)
                    return redirect('push:index')
                else:
                    return HttpResponse('Login Error')
            else:
                return HttpResponse('Login Error')
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
        try:
            EmailMessage(u'title', u'body', to = ['hoge@example.com']).send()
            return HttpResponse('Send your register email')
        except Exception as e:
            raise
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('accounts/forget.html', c)
