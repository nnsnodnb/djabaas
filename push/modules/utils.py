# coding=utf-8

from push.models import DeviceTokenModel, NotificationModel
from push.modules import push_notification

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
