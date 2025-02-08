import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    """
    Модель пользователя.
    """

    ROLE_CHOICES = [
        ("user", "Обычный пользователь"),
        ("admin", "Администратор"),
    ]

    oid = models.CharField(
        max_length=100,
        unique=True,
        default=uuid.uuid4,
        verbose_name="OID пользователя"
    )
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Команда пользователя",
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="user",
        verbose_name="роль в команде",
    )
    organization = models.ForeignKey(
        "teams.Organization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="organization_users",
        verbose_name="Организация",
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="custom_user_set",
    )

    def __str__(self):
        return self.username
