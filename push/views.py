from ast import literal_eval
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
from datetime import datetime
import json, urllib, ast, sys, os, threading, os.path

UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/files/'
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/modules')

import push_notification

@login_required(login_url = '/accounts/login/')
def index(request):
    device_tokens = DeviceTokenModel.objects.filter(username = request.user.username)
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
    notifications = NotificationModel.objects.filter(username = request.user.username)
    return render_to_response('push/notification_list.html',
                             {'notifications': notifications},
                             context_instance = RequestContext(request))

@login_required(login_url = '/accounts/login')
def notification_detail(request, notification_id):
    result = NotificationModel.objects.filter(id = notification_id)[0]
    return render_to_response('push/notification_detail.html',
                              {'result': result},
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
        if request.POST['datetime'] != '':
            notification.execute_datetime = request.POST['datetime']
        if request.POST.has_key('json'):
            notification.json = json.dumps(ast.literal_eval(request.POST['json'])).replace('\'', '\"')
        if request.POST.has_key('content-available'):
            notification.content_available = True
        if request.POST.has_key('is_production'):
            notification.is_production = True
        notification.username = request.user.username

        notification.save()

        if notification.execute_datetime == '{0:%Y/%m/%d %H:%M}'.format(datetime.now()):
            device_tokens = DeviceTokenModel.objects.filter(os_version__gte = notification.os_version,
                                                            username = request.user.username)

            t = threading.Thread(target = prepare_push_notification, args = (notification, device_tokens))
            t.start();

        return redirect('push:notification_list')
    else:
        return HttpResponseForbidden()

@login_required(login_url = '/accounts/login/')
def delete_device_token(request, device_token_id):
    DeviceTokenModel.objects.filter(id = device_token_id).delete()
    return redirect('push:index')

@login_required(login_url = '/accounts/login')
def detail_device_token(request, device_token_id):
    result = DeviceTokenModel.objects.filter(id = device_token_id)[0]
    return render_to_response('push/device_token_detail.html',
                             {'result': result},
                             context_instance = RequestContext(request))

@csrf_exempt
def device_token_register(request, username):
    if request.method == 'POST' and request.META['HTTP_USER_AGENT'] == 'iOS/nnsnodnb-mBaaS-Service':
        response_data = {}
        post_device_token, post_os_version = '', ''
        json_data = literal_eval(request.body)

        if json_data.has_key('device_token'):
            post_device_token = json_data['device_token']

        if json_data.has_key('os_version'):
            post_os_version = json_data['os_version']

        device_token_model = DeviceTokenModel.objects.filter(device_token = post_device_token,
                                                             username = username)

        if len(device_token_model) == 0 and post_device_token != '' and post_os_version != '':
            float_os_version = convert_float_os_version(post_os_version)

            insert_data = DeviceTokenModel(os_version = float_os_version,
                                           device_token = post_device_token,
                                           username = username)
            insert_data.save()

            response_data['result'] = 'success'
            response_data['message'] = '"' + post_device_token + '" is registered'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            float_os_version = convert_float_os_version(post_os_version)

            # Version down and Version up of iOS
            if device_token_model[0].os_version != float_os_version:
                device_token_model[0].os_version = float_os_version
                device_token_model[0].save()
            response_data['result'] = 'success'
            response_data['message'] = '"' + post_device_token + '" was registered'

            return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        # return HttpResponseForbidden()
        return HttpResponse('Access Denied', status=403)

def convert_float_os_version(os_version):
    try:
        return float(os_version['os_version'])
    except Exception as e:
        os_version_arrays = os_version.split('.')
        tmp_string = os_version_arrays[0] + '.' + os_version_arrays[1]
        return float(tmp_string)

def prepare_push_notification(notification, device_tokens):
    device_token_lists = []
    for item in device_tokens:
        device_token_lists.append(item.device_token)

    push_notification.execute(device_token_lists, notification)
