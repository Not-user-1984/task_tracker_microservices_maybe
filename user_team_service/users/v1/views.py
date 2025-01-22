from rest_framework import generics, permissions
from users.models import User
from users.v1.serializers import UserRegistrationSerializer, UserSerializer

# Регистрация пользователя
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

# Управление пользователем (обновление, удаление)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# Управление статусами пользователей (для администраторов)
class UserStatusUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

# Управление привязкой пользователей к команде (для администраторов)
class UserTeamUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]