from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.db.models import Q  

from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.serializers.users import UserCreateSerializer, UserSerializer
from core.utils.email import send_reset_password_email
from core.models import OrderService

User = get_user_model()


# =========================
# LOGIN CASE-INSENSITIVE (username OU email)
# =========================
class CaseInsensitiveTokenSerializer(TokenObtainPairSerializer):


    def validate(self, attrs):
        login_value = attrs.get(self.username_field)  # por padrão "username"
        password = attrs.get("password")

        if not login_value or not password:
            raise serializers.ValidationError(
                {"detail": "Usuário e senha são obrigatórios."}
            )

        try:
            # Busca por username OU email, ambos iexact (case-insensitive)
            user = User.objects.get(
                Q(username__iexact=login_value) | Q(email__iexact=login_value)
            )
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "Credenciais inválidas."})

        if not user.check_password(password):
            raise serializers.ValidationError({"detail": "Credenciais inválidas."})

        if not user.is_active or getattr(user, "is_deleted", False):
            raise serializers.ValidationError({"detail": "Usuário desativado."})

        # Gera os tokens manualmente para este user
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CaseInsensitiveTokenSerializer


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


# =========================
# REGISTER
# =========================
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"id": user.id, "username": user.username, "email": user.email},
            status=status.HTTP_201_CREATED,
        )


# =========================
# FORGOT / RESET PASSWORD
# =========================
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"detail": "Email é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_object_or_404(User, email=email)
        token = default_token_generator.make_token(user)

        frontend_url = request.data.get("frontend_url")
        reset_link = f"{frontend_url}?uid={user.pk}&token={token}"

        send_reset_password_email(email, reset_link)
        return Response({"detail": "Email de recuperação enviado."})


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        password = request.data.get("password")

        if not all([uid, token, password]):
            return Response(
                {"detail": "uid, token e password são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_object_or_404(User, pk=uid)

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Token inválido ou expirado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(password)
        user.save()
        return Response({"detail": "Senha redefinida com sucesso."})


# =========================
# /auth/me
# =========================
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retorna os dados do usuário autenticado.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        'Apaga' (soft delete) a conta do usuário autenticado.
        Mantém logs, marca OS como deletadas logicamente.
        """
        user = request.user

        # Marca ordens do usuário como deletadas logicamente
        OrderService.objects.filter(created_by=user).update(is_deleted=True)
        OrderService.objects.filter(updated_by=user).update(is_deleted=True)

        # Se você quiser, pode futuramente permitir null nas FKs e limpar:
        # OrderService.objects.filter(created_by=user).update(created_by=None)
        # OrderService.objects.filter(updated_by=user).update(updated_by=None)

        # Soft delete + anonimização do usuário (implementado no model User.delete())
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
