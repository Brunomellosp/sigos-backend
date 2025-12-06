from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from core.serializers.users import UserSerializer, UserCreateSerializer
from core.permissions.roles import IsAdmin

User = get_user_model()


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def perform_destroy(self, instance):
        if instance.is_admin():
            # 400 Bad Request com mensagem amigável
            raise ValidationError("Usuário ADMIN não pode ser deletado.")
        return super().perform_destroy(instance)
