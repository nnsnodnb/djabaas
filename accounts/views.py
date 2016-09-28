from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf

def register(request):
    if request.method == 'POST':
        return HttpResponse('hello')
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
