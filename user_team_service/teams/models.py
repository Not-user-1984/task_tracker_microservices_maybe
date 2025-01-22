from django.db import models
from users.models import User  # Импортируем кастомную модель пользователя


class Team(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(
        max_length=10, unique=True
    )  # Код для привязки пользователей

    def __str__(self):
        return self.name


class OrganizationalStructure(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="structures")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="positions")
    role = models.CharField(max_length=100)  # Роль в подразделении
    manager = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subordinates",
    )

    def __str__(self):
        return f"{self.user.username} - {self.role} in {self.team.name}"


class News(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="news")
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
