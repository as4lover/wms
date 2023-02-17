# Generated by Django 3.2.15 on 2023-01-17 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_order_representative'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='item_status',
            field=models.CharField(blank=True, choices=[('정상', '정상'), ('파손', '파손'), ('반품', '반품')], default='정상', max_length=100, null=True),
        ),
    ]
