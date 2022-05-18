from django.db import models
from .client   import Client
from .item   import Item
from django.utils import timezone

class Quotation(models.Model):
    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(default= timezone.localdate())
    iva = models.IntegerField('iva', default=19)
    discount = models.IntegerField('discount', default=0)
    subtotal = models.FloatField('subtotal', default=0)
    totalDiscount = models.FloatField('totalDiscount', default=0)
    totalIva = models.FloatField('totalIva', default=0)
    total = models.FloatField('total', default=0)

    def __str__(self):
        return str(self.id) + ' ' + ' ' + str(self.client) + ' ' + str(self.dateTime) + ' ' + str(self.iva) + ' ' + str(self.discount) + ' ' + str(self.subtotal) + ' ' + str(self.totalDiscount) + ' ' + str(self.totalIva) + ' ' + str(self.total)
