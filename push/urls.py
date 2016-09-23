from django.conf.urls import url
from push import views

urlpatterns = [
    # url(r'^$', views.index, name = 'index'),
    url(r'^register', views.device_token_register, name = 'device_token_register'),
]
