# coding: utf-8

from django.contrib import admin
from accounts.models import UserActivateTokenModel

class UserActivateTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'token')
    list_display_links = ('id', 'username')

admin.site.register(UserActivateTokenModel, UserActivateTokenAdmin)
