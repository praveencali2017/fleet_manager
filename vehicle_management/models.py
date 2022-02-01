from django.db import models
from loguru import logger
from fleetmanager.model_helpers import BaseMethod
from customer_management.models import Customer
# Create your models here.
VEHICLESTATUS_PK = 'vin_number'



class Vehicle(models.Model, BaseMethod):
    vin_number = models.CharField(primary_key=True, max_length=50)
    license_plate = models.CharField(max_length=50, null=True)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vehicles'
        indexes = [
            models.Index(fields=['owner_id']),
            models.Index(fields=['created_on']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['license_plate'])
        ]


class VehicleStatus(models.Model, BaseMethod):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    tires = models.JSONField(null=True)
    battery_level = models.IntegerField(null=True)
    fuel_level = models.IntegerField(null=True)
    gps_position = models.JSONField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vehicles_status'
        indexes = [
            models.Index(fields=['battery_level']),
            models.Index(fields=['fuel_level']),
            models.Index(fields=['created_on']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['vehicle_id'])
        ]

    @classmethod
    def create_or_update_vehicle(cls, key_identifiers: list, **kwargs):
        """
        Create or update model data, based on key_identifiers match. Updates values supplied in kwargs
        :param key_identifiers: matching keys
        :param kwargs: to be updated values
        :return: tuple (instance, True/False: created or not)
        """
        vehicle_data = dict()
        if VEHICLESTATUS_PK in kwargs:
            vehicle_data[VEHICLESTATUS_PK] = kwargs[VEHICLESTATUS_PK]
        if 'license_plate' in kwargs:
            vehicle_data['license_plate'] = kwargs['license_plate']
        vehicle_instance = None
        if vehicle_data:
            vehicle_instance, _ = Vehicle.create_or_update(key_identifiers, **vehicle_data)
        if not vehicle_instance:
            return None, False
        if 'vin_number' in kwargs:
            kwargs.pop('vin_number')
            kwargs['vehicle_id'] = vehicle_instance.vin_number
        instance, is_created = cls.create_or_update(['vehicle_id'], **kwargs)
        return instance, is_created

    def update_tires(self, tires: dict):
        for key, value in tires.items():
            self.tires[key] = value
        self.save()

    def update_gps_loc(self, gps_pos: dict):
        for key, value in gps_pos.items():
            self.gps_position[key] = value
        self.save()

    def update_individual_fields(self, **kwargs):
        need_tires_update = True if 'tires' in kwargs and kwargs['tires'] else False
        need_gps_loc_update = True if 'gps_position' in kwargs and kwargs['gps_position'] else False
        battery_level = kwargs.get('battery_level', None)
        fuel_level = kwargs.get('fuel_level', None)
        if need_tires_update:
            self.update_tires(kwargs['tires'])
        if need_gps_loc_update:
            self.update_gps_loc(kwargs['gps_position'])
        if battery_level is not None:
            self.battery_level = battery_level
            self.save()
        if fuel_level is not None:
            self.fuel_level = fuel_level
            self.save()


