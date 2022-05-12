from django.db import models
from .client   import Client
from .item   import Item
from django.utils import timezone


class Quotation(models.Model):
    id = models.BigAutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)
    price = models.FloatField('price', default=0)
    total = models.FloatField('total', default=0)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField('date', default=timezone.localdate)
    time = models.TimeField('time', default=timezone.localtime)
    iva = models.IntegerField('iva', default=19)
    discount = models.IntegerField('discount', default=0)

    def __str__(self):
        return self.id + ' ' + self.item + ' ' + self.quantity + ' ' + self.price + ' ' + self.total + ' ' + self.client + ' ' + self.date.strftime('%d/%m/%Y') + ' ' + self.time.strftime('%H:%M') + ' ' + self.iva + ' ' + self.discount
