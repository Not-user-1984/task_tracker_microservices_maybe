# Generated by Django 5.0.4 on 2025-01-27 07:45

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0006_userassignment_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='oid',
            field=models.CharField(default=uuid.uuid4, max_length=100, unique=True, verbose_name='OID новостей'),
        ),
        migrations.AddField(
            model_name='project',
            name='oid',
            field=models.CharField(default=uuid.uuid4, max_length=100, unique=True, verbose_name='OID проекта'),
        ),
        migrations.AddField(
            model_name='team',
            name='oid',
            field=models.CharField(default=uuid.uuid4, max_length=100, unique=True, verbose_name='OID команды'),
        ),
        migrations.AddField(
            model_name='userassignment',
            name='project_oid',
            field=models.UUIDField(editable=False, null=True),
        ),
    ]
