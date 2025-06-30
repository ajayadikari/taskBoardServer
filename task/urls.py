from django.urls import path
from .views import get_all_tasks, create_task, delete_task, update_task, update_task_status

urlPatterns = [
    path("get-all-tasks/", get_all_tasks), 
    path('create-task/', create_task), 
    path('delete-task/<str:task_id>/', delete_task), 
    path('update-task/<str:task_id>/', update_task), 
    path('update-task-status/<str:task_id>/<str:new_status>/', update_task_status)
]