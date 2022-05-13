from django.db import models
from .item   import Item
from .quotation import Quotation

class ItemsQuotation(models.Model):
    id = models.BigAutoField(primary_key=True)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)
    total = models.FloatField('total', default=0)

    def __str__(self):
        return str(self.id) + ' ' + str(self.quotation) + ' ' + str(self.item) + ' ' + str(self.quantity) + ' ' + str(self.total)
