from django.urls import path
from .views import get_report


urlPatterns = [
    path('<str:id>/export-pdf/', get_report)
]