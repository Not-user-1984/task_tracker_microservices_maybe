# Generated by Django 5.0.4 on 2025-01-24 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_userassignment_project_name_userassignment_team_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userassignment',
            name='user_email',
            field=models.CharField(blank=True, editable=False, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userassignment',
            name='user_name',
            field=models.CharField(blank=True, editable=False, max_length=255, null=True),
        ),
    ]
