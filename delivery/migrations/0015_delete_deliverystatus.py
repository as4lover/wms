# Generated by Django 3.2.15 on 2023-03-11 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0014_alter_deliverystatus_delivery_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DeliveryStatus',
        ),
    ]
