# coding: utf-8

from django.contrib import admin
from push.models import DeviceTokenModel, NotificationModel, DevelopFileModel, ProductFileModel

class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'os_version', 'device_token', 'register_datetime', 'update_datetime')
    list_display_links = ('id', 'os_version')

admin.site.register(DeviceTokenModel, DeviceTokenAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'register_date')
    list_display_links = ('id', 'title')

admin.site.register(NotificationModel, NotificationAdmin)

class DevelopFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'development_file_name')
    list_display_links = ('id', 'development_file_name')

admin.site.register(DevelopFileModel, DevelopFileAdmin)

class ProductFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'production_file_name')
    list_display_links = ('id', 'production_file_name')

admin.site.register(ProductFileModel, ProductFileAdmin)
