from rest_framework import serializers
from users.models import User
from teams.models import Team


class UserRegistrationSerializer(serializers.ModelSerializer):
    team_code = serializers.CharField(write_only=True, required=False)  # Код команды

    class Meta:
        model = User
        fields = ["username", "email", "password", "status", "team_code"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        team_code = validated_data.pop("team_code", None)
        user = User.objects.create_user(**validated_data)

        if team_code:
            try:
                team = Team.objects.get(code=team_code)
                user.team = team
                user.save()
            except Team.DoesNotExist:
                pass

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "status", "team"]
