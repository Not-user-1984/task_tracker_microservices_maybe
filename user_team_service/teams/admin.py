from django.contrib import admin
from .models import Organization, Project, Team, UserAssignment, News


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "admin")
    search_fields = ("name", "admin__username")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "organization")
    list_filter = ("organization",)
    search_fields = ("name", "organization__name")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "project")
    list_filter = ("project",)
    search_fields = ("name", "project__name")


@admin.register(UserAssignment)
class UserAssignmentAdmin(admin.ModelAdmin):
    list_display = ("user", "project", "team")
    list_filter = ("project", "team")
    search_fields = ("user__username", "project__name", "team__name")


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "team", "created_by", "created_at")
    list_filter = ("team", "created_by", "created_at")
    search_fields = ("title", "content", "team__name")

    def get_queryset(self, request):
        """
        Ограничиваем доступ к новостям: админ организации видит только новости своих команд.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == "admin" and request.user.organization:
            return qs.filter(team__project__organization=request.user.organization)
        return qs.none()

    def save_model(self, request, obj, form, change):
        """
        Автоматически назначаем создателя новости.
        """
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Ограничиваем выбор команд: админ организации может выбирать только свои команды.
        """
        if db_field.name == "team":
            if request.user.is_superuser:
                pass
            elif request.user.role == "admin" and request.user.organization:
                # Админ организации может выбирать только свои команды
                kwargs["queryset"] = Team.objects.filter(
                    project__organization=request.user.organization
                )
            else:
                kwargs["queryset"] = (
                    Team.objects.none()
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
