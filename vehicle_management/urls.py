from django.urls import path
from vehicle_management import views
urlpatterns = [
    path('vehicles/location', views.get_vehicles_by_location, name='geo_vehicle_lookup'),
    path('vehicles/<str:vin_number>', views.delete_vehicle_data, name='geo_vehicle_lookup'),
    path('vehicles/customer/<str:customer_id>', views.assign_vehicles_to_customer, name='assign_vehicles'),
    path('vehicles', views.create_update_vehicle_data, name='create_update_vehicle_data')
]
