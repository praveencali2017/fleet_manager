from django.urls import path
from file_manager import views
urlpatterns = [
    path('', views.file_upload, name='file_upload')
]
