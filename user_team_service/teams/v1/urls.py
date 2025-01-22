from django.urls import path
from .views import (
    TeamCreateView, TeamDetailView,
    OrganizationalStructureCreateView, OrganizationalStructureDetailView,
    NewsCreateView, NewsDetailView
)

urlpatterns = [
    # Управление командами
    path('teams/', TeamCreateView.as_view(), name='team-create'),
    path('teams/<int:pk>/', TeamDetailView.as_view(), name='team-detail'),

    # Управление организационной структурой
    path('structures/', OrganizationalStructureCreateView.as_view(), name='structure-create'),
    path('structures/<int:pk>/', OrganizationalStructureDetailView.as_view(), name='structure-detail'),

    # Управление новостями
    path('news/', NewsCreateView.as_view(), name='news-create'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
]