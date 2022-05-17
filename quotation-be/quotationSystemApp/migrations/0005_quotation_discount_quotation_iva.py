# Generated by Django 4.0.2 on 2022-05-11 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotationSystemApp', '0004_rename_input_item_quotation'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='discount',
            field=models.IntegerField(default=0, verbose_name='discount'),
        ),
        migrations.AddField(
            model_name='quotation',
            name='iva',
            field=models.IntegerField(default=19, verbose_name='iva'),
        ),
    ]