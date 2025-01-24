# Generated by Django 5.0.4 on 2025-01-23 10:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_news', to=settings.AUTH_USER_MODEL, verbose_name='Создатель новости'),
        ),
        migrations.AddField(
            model_name='organization',
            name='admin',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin_of_organization', to=settings.AUTH_USER_MODEL, verbose_name='Админ организации'),
        ),
        migrations.AddField(
            model_name='project',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='teams.organization', verbose_name='Организация'),
        ),
        migrations.AddField(
            model_name='team',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='teams.project', verbose_name='Проект'),
        ),
        migrations.AddField(
            model_name='news',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to='teams.team', verbose_name='Команда'),
        ),
        migrations.AddField(
            model_name='userassignment',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='teams.project', verbose_name='Проект'),
        ),
        migrations.AddField(
            model_name='userassignment',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignments', to='teams.team', verbose_name='Команда'),
        ),
        migrations.AddField(
            model_name='userassignment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
