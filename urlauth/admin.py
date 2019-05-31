from django.contrib import admin

from urlauth.models import AuthKey


class AuthKeyAdmin(admin.ModelAdmin):
    list_display = ['id', 'uid', 'expired']

admin.site.register(AuthKey, AuthKeyAdmin)
