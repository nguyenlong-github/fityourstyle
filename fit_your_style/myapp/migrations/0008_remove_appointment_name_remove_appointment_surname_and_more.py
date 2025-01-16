# Generated by Django 5.1.1 on 2024-12-24 12:54

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='name',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='surname',
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default=123, max_length=254, verbose_name='メールアドレス'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user'),
        ),
    ]