from django.contrib import admin
from .models import BoardModel

class BoardAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']

admin.site.register(BoardModel, BoardAdmin)