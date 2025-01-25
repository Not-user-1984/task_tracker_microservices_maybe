# Generated by Django 5.0.4 on 2025-01-24 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userassignment',
            name='project_name',
            field=models.CharField(editable=False, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userassignment',
            name='team_name',
            field=models.CharField(blank=True, editable=False, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userassignment',
            name='user_uuid',
            field=models.UUIDField(editable=False, null=True),
        ),
    ]
