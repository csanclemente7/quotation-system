# Generated by Django 4.0.2 on 2022-05-12 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotationSystemApp', '0010_quotation_subtotal_quotation_totaliva'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='totalDiscount',
            field=models.FloatField(default=0, verbose_name='totalDiscount'),
        ),
    ]
