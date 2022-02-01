from django.urls import path
from customer_management import views

urlpatterns = [
    path('customers', views.create_update_customer, name='create_update_customer'),
    path('customer', views.get_customer, name='fetch_customer'),
]

