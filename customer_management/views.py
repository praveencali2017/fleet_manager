from django.http import JsonResponse, HttpResponseServerError
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from loguru import logger
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.


@api_view(['GET'])
def get_customer(request):
    from customer_management.models import Customer
    customer_email = request.GET.get('customer_email', None)
    if customer_email is None:
        return JsonResponse({'success': False, 'msg': f'Email required!!!'})
    customer_email_lw = customer_email.lower()
    customer = Customer.get(email_address=customer_email_lw)
    if customer is None:
        return JsonResponse({'success': False, 'msg': f'Customer with email {customer_email} does not exists!!!'})
    data = model_to_dict(customer)
    return JsonResponse(data)


@api_view(['POST', 'PUT'])
@csrf_exempt
def create_update_customer(request):
    from vehicle_management.models import Customer
    customer_data = json.loads(request.body)
    if 'email_address' not in customer_data:
        return JsonResponse({'success': False, 'msg': f'Customer email is required!!!'})
    customer_data['email_address'] = customer_data['email_address'].lower()
    customer, is_created = Customer.create_or_update(key_identifiers=['email_address'], **customer_data)
    if customer and not is_created:
        return JsonResponse({'success': True, 'msg': f'Customer already exists with this email'
                                                     f' {customer.email_address} and other values are updated!!!'})
    if is_created:
        return JsonResponse({'success': True, 'msg': f'Customer with email {customer.email_address} is created!!!'})
    return HttpResponseServerError('Server error!!!')
