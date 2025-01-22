from django.urls import path, include

from django.contrib import admin


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("users.v1.urls")),
    path("api/v1/teams/", include("teams.v1.urls")),
]
