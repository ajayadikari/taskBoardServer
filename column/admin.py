from django.contrib import admin
from .models import ColumnModel


class ColumnAdmin(admin.ModelAdmin):
    list_display = ['id', 'board', 'status']

admin.site.register(ColumnModel, ColumnAdmin)