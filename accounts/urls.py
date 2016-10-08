# coding: utf-8

from django.conf.urls import url
from django.contrib.auth.views import login,logout
from accounts import views

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name = 'login'),
    url(r'^logout/$', logout, {'template_name': 'accounts/logout.html'}, name = 'logout'),
    url(r'^entry/$', views.register, name = 'register'),
    url(r'^forget/$', views.forget, name = 'forget'),
    url(r'^change_password/$', views.change_password, name='change_password'),
]
