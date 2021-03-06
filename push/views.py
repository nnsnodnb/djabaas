# coding: utf-8

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseForbidden, QueryDict
from push.models import DeviceTokenModel, NotificationModel, DevelopFileModel, ProductFileModel
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.template.context_processors import csrf
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from ast import literal_eval
from datetime import datetime
from user_agents import parse
from push.modules.enumerates import NotificationStatus
from enum import Enum
import json, urllib, ast, sys, os, threading, os.path, csv
from push.modules import utils

UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/files/'

@login_required(login_url = '/accounts/login/')
def index(request):
    device_tokens_list = DeviceTokenModel.objects.filter(username = request.user.username)
    paginator = Paginator(device_tokens_list, 20)

    page = request.GET.get('page')
    try:
        device_tokens = paginator.page(page)
    except PageNotAnInteger:
        device_tokens = paginator.page(1)
    except EmptyPage:
        device_tokens = paginator.page(paginator.num_pages)

    return render(request, 'push/top.html', {'device_tokens': device_tokens})

@login_required(login_url = '/accounts/login')
def download_device_token(request):
    device_tokens = DeviceTokenModel.objects.filter(username = request.user.username)

    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename="device_token_list.csv"'
    writer = csv.writer(response)
    writer.writerow(['OS Version', 'Device Token', 'Register Date'])

    for item in device_tokens:
        writer.writerow([str(item.os_version), item.device_token, '{0:%Y/%m/%d %H:%M}'.format(item.register_datetime)])

    return response

@login_required(login_url = '/accounts/login/')
def sender(request):
    if DevelopFileModel.objects.filter(upload_username = request.user.username).count() > 0 and ProductFileModel.objects.filter(upload_username = request.user.username).count() == 0:
        return render(request, 'push/sender.html', {'is_develop': True, 'is_product': False})
    elif DevelopFileModel.objects.filter(upload_username = request.user.username).count() == 0 and ProductFileModel.objects.filter(upload_username = request.user.username).count() > 0:
        return render(request, 'push/sender.html', {'is_develop': False, 'is_product': True})
    elif DevelopFileModel.objects.filter(upload_username = request.user.username).count() == 0 and ProductFileModel.objects.filter(upload_username = request.user.username).count() == 0:
        return render(request, 'push/sender.html', {'is_develop': False, 'is_product': False})
    else:
        return render(request, 'push/sender.html', {'is_develop': True, 'is_product': True})

@login_required(login_url = '/accounts/login/')
def notification_list(request):
    notifications_list = NotificationModel.objects.filter(username = request.user.username)
    paginator = Paginator(notifications_list, 20)

    page = request.GET.get('page')
    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        notifications = paginator.page(1)
    except EmptyPage:
        notifications = paginator.page(paginator.num_pages)
    return render(request, 'push/notification_list.html', {'notifications': notifications})

@login_required(login_url = '/accounts/login')
def notification_detail(request, notification_id):
    result = NotificationModel.objects.filter(id = notification_id)[0]
    return render(request, 'push/notification_detail.html', {'result': result})

@login_required(login_url = '/accounts/login')
def notification_modify(request):
    if request.method == 'POST':
        notification = NotificationModel.objects.filter(id = request.POST['notification_id'])[0]
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
            tmp_datetime = request.POST['datetime'].split(' ')
            date = tmp_datetime[0]
            hour = tmp_datetime[1].split(':')[0]
            minute = tmp_datetime[1].split(':')[1]
            is_fm = True if tmp_datetime[2] == u'午後' else False
            if is_fm:
                hour = str(int(hour) + 12)
            notification.execute_datetime = date + ' ' + hour + ':' + minute
        else:
            notification.execute_datetime = '{0:%Y/%m/%d %H:%M}'.format(datetime.now())
        if 'json' in request.POST:
            notification.json = json.dumps(ast.literal_eval(request.POST['json'])).replace('\'', '\"')
        if 'content-available' in request.POST:
            notification.content_available = True
        if 'is_production' in request.POST:
            notification.is_production = True

        notification.save()

        if notification.execute_datetime == '{0:%Y/%m/%d %H:%M}'.format(datetime.now()) or notification.execute_datetime == '':
            device_tokens = DeviceTokenModel.objects.filter(os_version__gte = notification.os_version,
                                                            username = request.user.username)

            t = threading.Thread(target = utils.prepare_push_notification, args = (notification, device_tokens))
            t.start();

        return redirect('push:notification_list')
    else:
        return redirect('push:notification_list')

@login_required(login_url = '/accounts/login/')
def settings(request):
    if request.method == 'POST' and ('development' in request.FILES or 'production' in request.FILES):
        if 'development' in request.FILES:
            file = request.FILES['development']
            pem_file = DevelopFileModel(upload_username = request.user.username,
                                        development_file_name = str(request.user.username) + '/' + file.name)
        elif 'production' in request.FILES:
            file = request.FILES['production']
            pem_file = ProductFileModel(upload_username = request.user.username,
                                        production_file_name = str(request.user.username) + '/' + file.name)

        if '.pem' not in file.name:
            return render(request, 'push/settings.html', {'result': 'wrong'})
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

        return render(request, 'push/settings.html', {'result': 'success'})
    else:
        is_develop = True if DevelopFileModel.objects.filter(upload_username = request.user.username).count() >= 1 else False
        is_product = True if ProductFileModel.objects.filter(upload_username = request.user.username).count() >= 1 else False
        return render(request, 'push/settings.html', {'is_develop': is_develop, 'is_product': is_product})

@csrf_exempt
@login_required(login_url = '/accounts/login/')
def delete_pem(request):
    if request.method == 'POST':
        if request.POST['pem_type'] == 'develop':
            develop_model = DevelopFileModel.objects.filter(upload_username = request.user.username)[0]
            os.remove(UPLOAD_DIR + develop_model.development_file_name)
            develop_model.delete()
            return render(request, 'push/settings.html')
        elif request.POST['pem_type'] == 'product':
            product_model = ProductFileModel.objects.filter(upload_username = request.user.username)[0]
            os.remove(UPLOAD_DIR + product_model.production_file_name)
            product_model.delete()
            return render(request, 'push/settings.html')
    else:
        result = request.GET['result']
        return render(request, 'push/settings.html', {'destory': result})

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
            tmp_datetime = request.POST['datetime'].split(' ')
            date = tmp_datetime[0]
            hour = tmp_datetime[1].split(':')[0]
            minute = tmp_datetime[1].split(':')[1]
            is_fm = True if tmp_datetime[2] == u'午後' else False
            if is_fm:
                hour = str(int(hour) + 12)
            notification.execute_datetime = date + ' ' + hour + ':' + minute
        else:
            notification.execute_datetime = '{0:%Y/%m/%d %H:%M}'.format(datetime.now())
        if 'json' in request.POST:
            notification.json = json.dumps(ast.literal_eval(request.POST['json'])).replace('\'', '\"')
        if 'content-available' in request.POST:
            notification.content_available = True
        if 'mutable-content' in request.POST:
            notification.mutable_content = True
        if 'is_production' in request.POST:
            notification.is_production = True
        notification.username = request.user.username

        notification.save()

        if notification.execute_datetime == '{0:%Y/%m/%d %H:%M}'.format(datetime.now()) or notification.execute_datetime == '':
            device_tokens = DeviceTokenModel.objects.filter(os_version__gte = notification.os_version,
                                                            username = request.user.username)

            t = threading.Thread(target = utils.prepare_push_notification, args = (notification, device_tokens))
            t.start();

            notification.is_sent = True
            notification.status = 1
            notification.save()

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
    return render(request, 'push/device_token_detail.html', {'result': result})

@csrf_exempt
def device_token_register(request, username):
    if request.method == 'POST' and request.META['HTTP_USER_AGENT'] == 'iOS/nnsnodnb-mBaaS-Service':
        response_data = {}
        post_device_token, post_os_version, post_uuid = '', '', ''
        json_data = literal_eval(request.body)

        if 'device_token' in json_data:
            post_device_token = json_data['device_token']

        if 'os_version' in json_data:
            post_os_version = json_data['os_version']

        if 'uuid' in json_data:
            post_uuid = json_data['uuid']

        device_token_model = DeviceTokenModel.objects.filter(username = username,
                                                             uuid = post_uuid)

        if device_token_model.count() == 0 and post_device_token != '' and post_os_version != '' and post_uuid != '':
            float_os_version = utils.convert_float_os_version(post_os_version)

            insert_data = DeviceTokenModel(os_version = float_os_version,
                                           device_token = post_device_token,
                                           username = username,
                                           uuid = post_uuid)
            insert_data.save()

            response_data['result'] = 'success'
            response_data['message'] = '"' + post_device_token + '" is registered'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            float_os_version = utils.convert_float_os_version(post_os_version)

            for model in device_token_model:
                if model.os_version != float_os_version:
                    model.os_version = float_os_version
                if model.device_token != post_device_token:
                    model.device_token = post_device_token
                model.update_datetime = datetime.now()
                model.save()

            response_data['result'] = 'success'
            response_data['message'] = '"' + post_device_token + '" is updated'

            return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        # return HttpResponseForbidden()
        return HttpResponse('Access Denied', status=403)

@csrf_exempt
@login_required(login_url = '/accounts/login')
def change_notification_status(request):
    if request.method == 'PUT':
        put_dict = {key: value[0] if len(value) == 1 else value for key, value in QueryDict(request.body).lists()}
        notification_id = put_dict['notification_id']
        status = put_dict['status']
        notification = NotificationModel.objects.filter(id = notification_id)[0]
        notification.status = int(status)
        notification.save()
        return redirect('push:notification_list')
    else:
        return redirect('push:notification_list')
