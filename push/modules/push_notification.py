import time
from apns import APNs, Frame, Payload
from push.models import DevelopFileModel, ProductFileModel

def execute_push_service(device_token_lists, notification):
    if notification.is_production:
        pem_file_name = ProductFileModel.objects.all()[0].production_file_name
        apns = APNs(use_sandbox = False, cert_file = pem_file_name, enhanced = True)
    else:
        pem_file_name = DevelopFileModel.objects.all()[0].development_file_name
        apns = APNs(use_sandbox = True, cert_file = pem_file_name, enhanced = True)

    token_hex = []
    for token in device_token_lists:
        token_hex.append(token)

    payload = Payload(alert = notification.message.decode('utf-8'),
                      sound = notification.sound,
                      badge = notification.badge,
                      custom = notification.json)

    frame = Frame()
    identifier = 1
    expiry = time.time() + 3600
    priority = 10

    for token in token_hex:
        frame.add_item(token, payload, identifier, expiry, priority)

    apns.gateway_server.send_notification_multiple(frame)
