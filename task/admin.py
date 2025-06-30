from django.contrib import admin
from .models import TaskModel


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'column', 'created_at', 'updated_at']

admin.site.register(TaskModel, TaskAdmin)