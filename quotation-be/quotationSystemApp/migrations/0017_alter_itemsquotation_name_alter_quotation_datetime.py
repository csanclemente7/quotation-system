# Generated by Django 4.0.2 on 2022-06-25 15:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotationSystemApp', '0016_alter_client_email_alter_client_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemsquotation',
            name='name',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='dateTime',
            field=models.DateTimeField(default=datetime.date(2022, 6, 25)),
        ),
    ]
