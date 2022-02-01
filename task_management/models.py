from django.db import models
from fleetmanager.model_helpers import BaseMethod
from customer_management.models import Customer
from loguru import logger
import uuid
# Create your models here.


# Use on fly, define rule or use existing ones for future tasks
class Rule(models.Model, BaseMethod):
    class RuleAction(models.TextChoices):
        SEND_EMAIL = ('send_email', 'Send_Email')
        STORE_LOG = ('store_log', 'Store_Log')
        CREATE_TASK = ('create_task', 'Create_Task')
    action = models.CharField(choices=RuleAction.choices, null=True, max_length=20)
    pattern_key = models.CharField(max_length=50, null=True)  # unique key used to search tables like vin_number etc
    model_name = models.CharField(max_length=20, null=True)
    attributes = models.JSONField(null=True)  # should be model fields as keys and values as dict of (operator and value)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rules'
        indexes = [
            models.Index(fields=['action']),
            models.Index(fields=['pattern_key']),
            models.Index(fields=['model_name']),
            models.Index(fields=['created_on']),
            models.Index(fields=['updated_at'])
        ]


class Task(models.Model, BaseMethod):
    # We can extend this in future
    class TaskStatus(models.TextChoices):
        CREATED = ('created', 'Created')
        COMPLETE = ('complete', 'Complete')
        CANCELED = ('canceled', 'Canceled')
    name = models.CharField(max_length=20)
    data_signature = models.CharField(max_length=80, null=True)

    class TaskCreator(models.TextChoices):
        CUSTOMER = ('customer', 'Customer')
        SYSTEM = ('system', 'System')
    created_entity = models.CharField(max_length=15, default=TaskCreator.CUSTOMER)
    created_by_task = models.ForeignKey("Task", null=True, on_delete=models.SET_NULL)
    rule = models.ForeignKey(Rule, null=True, on_delete=models.SET_NULL)
    status = models.CharField(choices=TaskStatus.choices, null=True, max_length=15,
                              default=TaskStatus.CREATED)
    created_by = models.ForeignKey(Customer, related_name="task_created_by", on_delete=models.CASCADE, null=True)
    assigned_to = models.ForeignKey(Customer, related_name="task_assigned_to", on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tasks'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['status']),
            models.Index(fields=['created_by_task']),
            models.Index(fields=['created_by']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['created_on']),
            models.Index(fields=['updated_at'])
        ]

    def to_json(self, required_fields=["name", "id", "status", "created_by_id", "assigned_to_id", "created_on"]):
        data = dict()
        for attr in required_fields:
            try:
                data[attr] = getattr(self, attr)
            except KeyError as e:
                logger.error(str(e))
        return data





