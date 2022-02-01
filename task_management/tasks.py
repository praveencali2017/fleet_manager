from fleetmanager import celery_app
from loguru import logger


@celery_app.task
def update_task_rule(task_id, pattern, pattern_key, model_name):
    """
    Updates rule and task based on actions
    :param task_id: current task id
    :param pattern: pattern to validate (usually follows this convention {'column_key':{'operator': value}})
    :param pattern_key: usually pk of the given model name
    :param model_name: model name on which task is being performed
    :return: None
    """
    from task_management.task_helpers import build_query_from_pattern, trigger_actions
    from task_management.models import Task
    rule_met = build_query_from_pattern(pattern, pattern_key, model_name)
    if rule_met:
        task = Task.get(id=task_id)
        rule = task.rule
        if task is None:
            logger.error(f'Rule has been met!!! but no relevant task: {task.id}')
            return
        # Take actions if rule has actions attached!!!
        trigger_actions(rule, task)
        task.status = Task.TaskStatus.COMPLETE
        task.save()
        logger.info(f"Task rule is met and updated. Pattern met: {pattern}!!!")


@celery_app.task
def check_tasks():
    """
    Cron job to check open tasks and see if rules are met
    :return: None
    """
    from task_management.models import Task
    from django.db.models import Q
    clause = Q(rule_id__isnull=False) & (Q(status__isnull=True) | Q(status=Task.TaskStatus.CREATED))
    tasks = Task.get_all_Q(clause)
    for task in tasks:
        rule = task.rule
        pattern = rule.attributes
        pattern_key = rule.pattern_key
        model_name = rule.model_name
        update_task_rule.delay(task.id, pattern, pattern_key, model_name)


