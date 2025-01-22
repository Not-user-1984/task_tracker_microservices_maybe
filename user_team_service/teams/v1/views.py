from rest_framework import generics, permissions
from teams.models import Team, OrganizationalStructure, News
from .serializers import (
    TeamSerializer,
    OrganizationalStructureSerializer,
    NewsSerializer,
)


# Управление командами
class TeamCreateView(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAdminUser]


class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]


# Управление организационной структурой
class OrganizationalStructureCreateView(generics.CreateAPIView):
    queryset = OrganizationalStructure.objects.all()
    serializer_class = OrganizationalStructureSerializer
    permission_classes = [permissions.IsAdminUser]


class OrganizationalStructureDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrganizationalStructure.objects.all()
    serializer_class = OrganizationalStructureSerializer
    permission_classes = [permissions.IsAuthenticated]


# Управление новостями
class NewsCreateView(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAdminUser]


class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]
