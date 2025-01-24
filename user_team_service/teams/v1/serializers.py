from rest_framework import serializers
from teams.models import Team, Organization, News


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "code"]


class OrganizationalStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "team", "user", "role", "manager"]


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["id", "team", "title", "content", "created_at"]
