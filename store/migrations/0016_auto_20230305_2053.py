# Generated by Django 3.2.15 on 2023-03-05 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0015_amidaily_created_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyJobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daily_merged_csv', models.FileField(blank=True, upload_to='order/daily/%Y/%m/%d/')),
                ('daily_merged_pdf', models.FileField(blank=True, upload_to='order/daily/pdf/%Y/%m/%d')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
        ),
        migrations.DeleteModel(
            name='amiDaily',
        ),
    ]
