# Generated by Django 4.0.2 on 2022-05-12 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotationSystemApp', '0006_remove_quotation_date_remove_quotation_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='discount',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='discount'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='iva',
            field=models.IntegerField(blank=True, default=19, null=True, verbose_name='iva'),
        ),
    ]