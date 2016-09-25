from django.contrib import admin
from push.models import DeviceTokenModel, NotificationModel

class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'os_version', 'device_token', 'register_datetime', 'update_datetime')
    list_display_links = ('id', 'os_version')

admin.site.register(DeviceTokenModel, DeviceTokenAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'register_date')
    list_display_links = ('id', 'title')

admin.site.register(NotificationModel, NotificationAdmin)
