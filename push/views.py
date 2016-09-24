from django.http import HttpResponse, HttpResponseForbidden
from push.models import DeviceTokenModel
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from user_agents import parse
import json

def index(request):
    device_tokens = DeviceTokenModel.objects.all()
    return render_to_response('push/top.html',
                             {'device_tokens': device_tokens},
                             context_instance = RequestContext(request))

def sender(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('push/sender.html', c)

def notification_thread(request):
    return HttpResponse('notification_thread')

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
