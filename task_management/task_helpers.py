import hmac
import hashlib
import base64
from loguru import logger
from fleetmanager.settings import TASK_KEY_GEN
import json
from task_management.models import Task, Rule

def gen_unique_key_from_data(data:dict, inject_key=False):
    key = TASK_KEY_GEN.encode('utf-8')
    data_bytes = json.dumps(data).encode('utf-8')
    digest = hmac.new(key, data_bytes, hashlib.sha256).digest()
    data_sig = base64.b64encode(digest).decode()
    if inject_key:
        data.update({'data_signature': data_sig})
    return data_sig


def update_task_rule_data(task_data):
    from loguru import logger
    from task_management.models import Task, Rule
    rule = None
    msg = ''
    if 'rule' in task_data:
        rule_values = {**task_data['rule']}
        # Todo: In future we can keep rules as unique patterns, now it creates duplicate patterns
        # if request with same data is made multiple times
        rule, _ = Rule.create_or_update(key_identifiers=['id'], **rule_values)
        task_data.pop('rule')
        logger.info(f'New rule with pattern: {rule_values} has been created!!!')
    logger.info(task_data)
    task, is_created = Task.create_or_update(key_identifiers=['id'], **task_data)
    logger.info(f"Task: {task.id} with name: {task.name} is created:{is_created}")
    if rule:
        task.rule_id = rule
        task.save()
    msg = f'Task has been created/updated!!!'
    logger.info(msg)
    return True, msg


#Todo: Supports >, < and = , in future we can extend this

def supported_operations(key, operation):
    if operation == "gt":
        return f"{key}__gt"
    elif operation == "lt":
        return f"{key}__lt"
    elif operation == "eq":
        return key


def build_query_from_pattern(pattern: dict, pattern_key, model_name):
    if "vehiclestatus".lower() == model_name.lower():
        from vehicle_management.models import VehicleStatus
        filters = {'vehicle_id': pattern_key}
        vehicle_status = VehicleStatus.get(**filters)
        if vehicle_status is None:
            logger.info(f'Vehicle status for vin: {pattern_key} is not yet available!!!')
            return False
        for key, value in pattern.items():
            column_name = key.split("__")[0]  # if json, then use django key based search approach
            if column_name in VehicleStatus.__dict__.keys():
                for operation, val in value.items():
                    filter_clause = supported_operations(key, operation)
                    filters[filter_clause] = val
        logger.info(filters)
        status_counts = VehicleStatus.get_count(**filters)
        logger.info(f'Count>>>{status_counts}')
        if status_counts > 0:
            return True
        return False

# Note: In real scenario this action triggers can be sent to background worker
def trigger_actions(rule: Rule, task: Task):
    """
    Same rule engine. Takes different route based on actions assigned
    :param rule: Rule data object
    :param task: Task data object
    :return:
    """
    if rule is None or task is None:
        logger.error(f"trigger_actions>>> Cannot trigger actions if tasks and/or rule is/are none!!!")
    if rule.action == Rule.RuleAction.CREATE_TASK:
        basic_param = {'name': f'Created by {task.id}',
                       'status': Task.TaskStatus.CREATED,
                       'created_by_task_id': task.id,
                       'created_entity': Task.TaskCreator.SYSTEM}
        data_key = gen_unique_key_from_data(basic_param, inject_key=True)
        existing_task = Task.get(data_signature=data_key)
        if existing_task is None:
            new_task, _ = Task.create_or_update(key_identifiers=['data_signature'], **basic_param)
            logger.info(f"New task {new_task.id} got created from {task.id}")
    elif rule.action == Rule.RuleAction.SEND_EMAIL:
        customer = task.created_by
        if customer:
            logger.info(f"Sending email to the task creator at {customer.email_address}")
        else:
            logger.info(f"No task owner attached. Cannot send email to the customer!!!")
    elif rule.action == Rule.RuleAction.STORE_LOG:
        logger.info(f"Storing log for the task: {task.id}")
