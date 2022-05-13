from django.db import models


class Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('name',max_length=100)
    price = models.FloatField('price', default=0)

    def __str__(self):
        return str(self.id) + ' ' + str(self.name) + ' ' + str(self.price)
