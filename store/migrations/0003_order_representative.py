# Generated by Django 3.2.15 on 2023-01-17 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_remove_order_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='representative',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
