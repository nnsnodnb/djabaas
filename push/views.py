from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from push.models import DeviceTokenModel, NotificationModel, DevelopFileModel, ProductFileModel
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.template.context_processors import csrf
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from user_agents import parse
import json, urllib, ast, sys, os, threading, os.path

UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/files/'
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/modules')

import push_notification

@login_required(login_url = '/accounts/login/')
def index(request):
    device_tokens = DeviceTokenModel.objects.all()
    return render_to_response('push/top.html',
                             {'device_tokens': device_tokens},
                             context_instance = RequestContext(request))

@login_required(login_url = '/accounts/login/')
def sender(request):
    c = {}
    c.update(csrf(request))
    if len(DevelopFileModel.objects.filter(upload_username = request.user.username)) > 0 and len(ProductFileModel.objects.filter(upload_username = request.user.username)) == 0:
        return render_to_response('push/sender_develop.html', c)
    elif len(DevelopFileModel.objects.filter(upload_username = request.user.username)) == 0 and len(ProductFileModel.objects.filter(upload_username = request.user.username)) > 0:
        return render_to_response('push/sender_product.html', c)
    elif len(DevelopFileModel.objects.filter(upload_username = request.user.username)) == 0 and len(ProductFileModel.objects.filter(upload_username = request.user.username)) == 0:
        return render_to_response('push/sender_none.html', c)
    else:
        return render_to_response('push/sender.html', c)

@login_required(login_url = '/accounts/login/')
def notification_list(request):
    notifications = NotificationModel.objects.all()
    return render_to_response('push/notification_list.html',
                             {'notifications': notifications},
                             context_instance = RequestContext(request))

@login_required(login_url = '/accounts/login/')
def settings(request):
    if request.method == 'POST' and (request.FILES.has_key('development') or request.FILES.has_key('production')):
        if request.FILES.has_key('development'):
            file = request.FILES['development']
            pem_file = DevelopFileModel(upload_username = request.user.username,
                                        development_file_name = str(request.user.username) + '/' + file.name)
        elif request.FILES.has_key('production'):
            file = request.FILES['production']
            pem_file = ProductFileModel(upload_username = request.user.username,
                                        production_file_name = str(request.user.username) + '/' + file.name)

        if '.pem' not in file.name:
            return redirect('push:settings')
        else:
            USER_UPLOAD_DIR = UPLOAD_DIR + str(request.user.username) + '/'
            if os.path.isdir(USER_UPLOAD_DIR) == False:
                os.mkdir(USER_UPLOAD_DIR)
            path = os.path.join(USER_UPLOAD_DIR, file.name)
            destination = open(path, 'wb')
            for chunk in file.chunks():
                destination.write(chunk)

            if isinstance(pem_file, DevelopFileModel):
                results = DevelopFileModel.objects.all()
                for item in results:
                    if os.path.isfile(USER_UPLOAD_DIR + item.development_file_name):
                        os.remove(USER_UPLOAD_DIR + item.development_file_name)
                DevelopFileModel.objects.all().delete()
            elif isinstance(pem_file, ProductFileModel):
                results = ProductFileModel.objects.all()
                for item in results:
                    if os.path.isfile(USER_UPLOAD_DIR + item.production_file_name):
                        os.remove(USER_UPLOAD_DIR + item.production_file_name)
                ProductFileModel.objects.all().delete()
            pem_file.save()

        return redirect('push:settings')
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('push/settings.html', c)

@login_required(login_url = '/accounts/login/')
def notification(request):
    if request.method == 'POST':
        notification = NotificationModel()
        if request.POST['title'] != '':
            notification.title = urllib.unquote(request.POST['title'])
        if request.POST['message'] != '':
            notification.message = urllib.unquote(request.POST['message'])
        if request.POST['os_version'] != '':
            notification.os_version = urllib.unquote(request.POST['os_version'])
        if request.POST['sound'] != '':
            notification.sound = request.POST['sound']
        if request.POST['badge'] != '':
            notification.badge = request.POST['badge']
        elif request.POST['badge'] == '':
            notification.badge = 0
        if request.POST['url'] != '':
            notification.url = urllib.unquote(request.POST['url'])
        if request.POST.has_key('json'):
            notification.json = json.dumps(ast.literal_eval(request.POST['json'])).replace('\'', '\"')
        if request.POST.has_key('content-available'):
            notification.content_available = True
        if request.POST.has_key('is_production'):
            notification.is_production = True

        notification.save()
        device_tokens = DeviceTokenModel.objects.filter(os_version__gte = notification.os_version)

        t = threading.Thread(target = prepare_push_notification, args = (notification, device_tokens))
        t.start();

        return redirect('push:notification_list')
    else:
        return HttpResponseForbidden()

@csrf_exempt
def device_token_register(request):
    if request.method == 'POST':# and request.META['HTTP_USER_AGENT'] == 'iOS/nnsnodnb-mBaaS-Service':
        receive_json = json.loads(request.body)
        insert_data = DeviceTokenModel(os_version = receive_json['os_version'],
                                       device_token = receive_json['device_token'])
        insert_data.save()

        response_data = {}
        response_data['result'] = 'success'
        response_data['message'] = '"' + receive_json['device_token'] + '" is registered'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseForbidden()

def prepare_push_notification(notification, device_tokens):
    device_token_lists = []
    for item in device_tokens:
        device_token_lists.append(item.device_token)

    push_notification.execute(device_token_lists, notification)
