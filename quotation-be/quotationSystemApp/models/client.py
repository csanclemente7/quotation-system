from django.db import models


class Client(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('name',max_length=100)
    city = models.CharField('city',max_length=100)
    address = models.CharField('address',max_length=100)
    email = models.CharField('email',max_length=100,blank=True, null=True)
    phone = models.CharField('phone',max_length=100, default=None,blank=True, null=True)

    def __str__(self):
        return str(self.id) + ' ' + str(self.name) + ' ' + str(self.city) + ' ' + str(self.address) + ' ' + str(self.email) + ' ' + str(self.phone)
