from django.db import models


class Client(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('name',max_length=100)
    city = models.CharField('city',max_length=100)
    address = models.CharField('address',max_length=100)
    email = models.EmailField('email',max_length=100)
    phone = models.CharField('phone',max_length=100, default=None)

    def __str__(self):
        return self.id + ' ' + self.name + ' ' + self.city + ' ' + self.address + ' ' + self.email + ' ' + self.phone
