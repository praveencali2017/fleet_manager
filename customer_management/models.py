from django.db import models
from fleetmanager.model_helpers import BaseMethod
# Create your models here.


class Customer(models.Model, BaseMethod):
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=30, null=True)
    email_address = models.EmailField(unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Just to make sure email is always in lowercase
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.email_address = self.email_address.lower()
        return super(Customer, self).save(force_insert, force_update, using,
                                          update_fields)

    class Meta:
        db_table = 'customers'
        indexes = [
            models.Index(fields=['email_address']),
            models.Index(fields=['first_name']),
            models.Index(fields=['last_name']),
            models.Index(fields=['created_on']),
            models.Index(fields=['updated_at'])
        ]
