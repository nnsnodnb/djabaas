from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf

def register(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('accounts/register.html', c)

def forget(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('accounts/forget.html', c)
