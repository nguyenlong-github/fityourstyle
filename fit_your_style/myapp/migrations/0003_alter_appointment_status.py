# Generated by Django 5.1.1 on 2024-12-06 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_appointment_create_at_appointment_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(default='pending', max_length=10, verbose_name='ステータス'),
        ),
    ]
