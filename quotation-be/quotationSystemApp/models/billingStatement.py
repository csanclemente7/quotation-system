from django.db import models
from .client   import Client
from .item   import Item
from django.utils import timezone
from .quotation import Quotation

class BillingStatement(models.Model):
    id = models.BigAutoField(primary_key=True)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' ' + ' ' + str(self.quotation)
