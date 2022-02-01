from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseBadRequest
import json
from rest_framework.decorators import api_view


@api_view(['PUT'])
@csrf_exempt
def assign_vehicles_to_customer(request, customer_id):
    from customer_management.models import Customer
    from vehicle_management.models import Vehicle
    data = json.loads(request.body)
    if 'vin_numbers' not in data and 'customer_email' not in data:
        return HttpResponseBadRequest('Need vin number(s) and customer email to map the vehicle(s) to customer')
    customer = Customer.get(id = customer_id)
    if customer is None:
        return HttpResponseBadRequest(f'Customer with {customer_id} does not exists!!!')
    provided_vin_numbers = data['vin_numbers']
    found_vin_numbers = []
    for vin_number in provided_vin_numbers:
        vehicle = Vehicle.get(vin_number=vin_number)
        if vehicle is not None:
            vehicle.owner = customer
            vehicle.save()
            found_vin_numbers.append(vehicle.vin_number)
    if len(provided_vin_numbers) != len(found_vin_numbers):
        missed_vins = list(set(provided_vin_numbers) - set(found_vin_numbers))
        return JsonResponse({'success': True, 'msg': f'Could not found vehicles with vin number(s): {missed_vins}.'
                                                     f' Rest are mapped to customer!!!'})
    return JsonResponse({'success': True, 'msg': 'All given vehicle(s) is/are mapped to the customer '})


@api_view(['GET'])
def get_vehicles_by_location(request):
    from vehicle_management.models import VehicleStatus
    latitude = request.GET.get('lat', None)
    longitude = request.GET.get('lon', None)
    if latitude is None or longitude is None:
        return JsonResponse({'success': False, 'msg': 'Need all longitude,latitude and customer_email values!!!'})
    vehicles_status = VehicleStatus.get_all(gps_position__lat=float(latitude),
                                       gps_position__lng=float(longitude))
    data = []
    for status in vehicles_status:
        record = {'license_plate': status.vehicle.license_plate, **model_to_dict(status)}
        if 'vehicle' in record:
            record['vin_number'] = record.pop('vehicle')
        data.append(record)
    return JsonResponse({'data': data, 'success': True})


@api_view(['POST', 'PUT'])
@csrf_exempt
def create_update_vehicle_data(request):
    from vehicle_management.models import Vehicle, VehicleStatus
    data = json.loads(request.body)
    if 'vin_number' not in data:
        return JsonResponse({'success': False, 'msg': 'vin_number is required !!!'})
    vehicle, is_created = Vehicle.create_or_update(key_identifiers=['vin_number'], **data)
    vehicle_status = VehicleStatus.get(vehicle=vehicle)
    # Need to change the key for vehicle status. From vin_number to vehicle_id
    vehicle_data_values = data.copy()
    vehicle_data_values['vehicle_id'] = vehicle_data_values.pop('vin_number')
    if vehicle_status is None:
        vehicle_status, _ = VehicleStatus.create_or_update(key_identifiers=['vehicle_id'], **vehicle_data_values)
    else:
        vehicle_status.update_individual_fields(**vehicle_data_values)
    record = {'license_plate': vehicle_status.vehicle.license_plate, **model_to_dict(vehicle_status)}
    if 'vehicle' in record:
        record['vin_number'] = record.pop('vehicle')
    return JsonResponse({'data': record, 'success': True})


@api_view(['DELETE'])
@csrf_exempt
def delete_vehicle_data(request, vin_number):
    from vehicle_management.models import Vehicle
    is_deleted = Vehicle.delete_objects(vin_number=vin_number)
    if not is_deleted:
        return JsonResponse({'success': False, 'msg': f'Cannot delete the vehicle data for vin number: {vin_number}'})
    return JsonResponse({'success': True, 'msg': f'Records of vehicle with vin number: {vin_number} got deleted!!!'})

