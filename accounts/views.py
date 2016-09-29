from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template.context_processors import csrf
import urllib

def register(request):
    if request.method == 'POST':
        arrays = request.body.split('&')
        query = {}
        for item in arrays:
            tmp_arrays = item.split('=')
            query[tmp_arrays[0]] = tmp_arrays[1]

        if query['password'] == query['password_confirm']:
            user = User(username = query['username'],
                        email = urllib.unquote(query['email']),
                        password = query['password'])
            user.save()
            return render_to_response('/accounts/login/next=/')
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
