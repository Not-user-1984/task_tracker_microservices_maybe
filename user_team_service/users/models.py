from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    STATUS_CHOICES = [
        ('user', 'Обычный пользователь'),
        ('admin', 'Администратор'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='user')
    team = models.ForeignKey('teams.Team', on_delete=models.SET_NULL, null=True, blank=True)

    # Указываем уникальные related_name для groups и user_permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='custom_user_set',  # Уникальное имя для обратной ссылки
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  # Уникальное имя для обратной ссылки
        related_query_name='user',
    )

    def __str__(self):
        return self.username