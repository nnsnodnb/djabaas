from django.conf.urls import url
from push import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^sender', views.sender, name = 'sender'),
    url(r'^notification_list', views.notification_list, name = 'notification_list'),
    url(r'^settings', views.settings, name = 'settings'),
    url(r'^notification_thread', views.notification_thread, name = 'notification_thread'),
    url(r'^register', views.device_token_register, name = 'device_token_register'),
]
