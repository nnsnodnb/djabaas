# coding=utf-8

import time, os, json
from apns import APNs, Frame, Payload
from push.models import DevelopFileModel, ProductFileModel
from django.conf import settings

PEM_FILE_DIR = settings.BASE_DIR + '/push/files/'

def execute(device_token_lists, notification):
    if notification.is_production:
        pem_file_name = ProductFileModel.objects.all()[0].production_file_name
        apns = APNs(use_sandbox = False, cert_file = PEM_FILE_DIR + pem_file_name, enhanced = True)
    else:
        pem_file_name = DevelopFileModel.objects.all()[0].development_file_name
        apns = APNs(use_sandbox = True, cert_file = PEM_FILE_DIR + pem_file_name, enhanced = True)

    token_hex = []
    for token in device_token_lists:
        token_hex.append(token)

    json_data = ''
    if notification.json != '':
        json_data = json.loads(notification.json)

    if notification.content_available:
        json_data['content-avalilable'] = 1

    payload = Payload(alert = notification.message,
                      sound = notification.sound,
                      badge = notification.badge,
                      custom = json_data)

    frame = Frame()
    identifier = 1
    expiry = time.time() + 3600
    priority = 10

    for token in token_hex:
        frame.add_item(token, payload, identifier, expiry, priority)

    apns.gateway_server.send_notification_multiple(frame)

    notification.is_sent = True
    notification.save()
