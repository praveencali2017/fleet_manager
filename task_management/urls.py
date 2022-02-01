from django.urls import path
from task_management import views

urlpatterns = [
    path('tasks', views.create_update_task, name='create_update_task'),
    path('tasks/customers', views.get_tasks_by_customer, name='get_customer_tasks')
]

