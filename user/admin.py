from django.contrib import admin
from .models import UserModel


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email']

admin.site.register(UserModel, UserAdmin)