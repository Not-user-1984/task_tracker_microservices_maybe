from django.db import models
from users.models import User


class Organization(models.Model):
    """
    Модель организации.
    """

    name = models.CharField(max_length=100, verbose_name="Название организации")
    admin = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admin_of_organization",
        verbose_name="Админ организации",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


class Project(models.Model):
    """
    Модель проекта.
    """

    name = models.CharField(max_length=100, verbose_name="Название проекта")
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name="Организация",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class Team(models.Model):
    """
    Модель команды.
    """

    name = models.CharField(max_length=100, verbose_name="Название команды")
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="teams", verbose_name="Проект"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"


class UserAssignment(models.Model):
    """
    Модель для назначения пользователей на проекты и в команды.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name="Пользователь",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name="Проект",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assignments",
        verbose_name="Команда",
    )

    user_oid = models.UUIDField(editable=False, null=True)
    project_name = models.CharField(max_length=255, editable=False, null=True)
    team_name = models.CharField(max_length=255, editable=False, null=True, blank=True)
    user_email = models.CharField(max_length=255, editable=False, null=True, blank=True)
    user_name = models.CharField(max_length=255, editable=False, null=True, blank=True)
    user_role = models.CharField(max_length=10, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.user_oid = self.user.oid
        self.project_name = self.project.name
        self.team_name = self.team.name if self.team else None
        self.user_email = self.user.email
        self.user_name = self.user.username
        self.user_role = self.user.role
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} -> {self.project.name} ({self.team.name if self.team else 'без команды'})"

    class Meta:
        verbose_name = "Назначение пользователя"
        verbose_name_plural = "Назначения пользователей"


class News(models.Model):
    """
    Модель для новостей, связанных с командой.
    """

    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="news", verbose_name="Команда"
    )
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_news",
        verbose_name="Создатель новости",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
