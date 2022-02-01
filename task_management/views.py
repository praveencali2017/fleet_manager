from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from loguru import logger
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
import json


@api_view(['POST', 'PUT'])
@csrf_exempt
def create_update_task(request):
    from task_management.models import Task
    from task_management.task_helpers import gen_unique_key_from_data, update_task_rule_data
    task_data = json.loads(request.body)
    data_key = gen_unique_key_from_data(task_data, inject_key=True)
    task = Task.get(data_signature=data_key)
    if task is not None and (task.status != Task.TaskStatus.COMPLETE.value or task.status != Task.TaskStatus.CANCELED.value):
        return JsonResponse({'success': False, 'msg': 'Already there is an existing open task with the same data.'
                                                      'Please complete or cancel the existing task to add new one!!!'})
    is_success, msg = update_task_rule_data(task_data)
    return JsonResponse({'success': is_success, 'msg': msg})



@api_view(['GET'])
def get_tasks_by_customer(request):
    from task_management.models import Task
    task_owner_id = request.GET.get('created_by_id', None)
    task_assigned_id = request.GET.get('assigned_to_id', None)
    search_data = dict()
    if task_owner_id is not None:
        search_data.update({'created_by_id': task_owner_id})
    if task_assigned_id is not None:
        search_data.update({'assigned_to_id': task_owner_id})
    tasks = Task.get_all(**search_data)
    logger.info(tasks)
    data = [task.to_json() for task in tasks]
    return JsonResponse({'status': True, 'data': data})




