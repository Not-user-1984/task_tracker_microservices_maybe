from rest_framework import generics, permissions
from users.models import User
from users.v1.serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserStatusUpdateSerializer,
    UserTeamUpdateSerializer,
)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserStatusUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserStatusUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


class UserTeamUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserTeamUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
