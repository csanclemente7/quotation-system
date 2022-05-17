# Generated by Django 4.0.2 on 2022-05-12 15:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quotationSystemApp', '0005_quotation_discount_quotation_iva'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotation',
            name='date',
        ),
        migrations.RemoveField(
            model_name='quotation',
            name='item',
        ),
        migrations.RemoveField(
            model_name='quotation',
            name='price',
        ),
        migrations.RemoveField(
            model_name='quotation',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='quotation',
            name='time',
        ),
        migrations.AddField(
            model_name='quotation',
            name='dateTime',
            field=models.DateTimeField(default=django.utils.timezone.localtime),
        ),
    ]