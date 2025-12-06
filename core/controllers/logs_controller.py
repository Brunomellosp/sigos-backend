from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from core.models import OrderService, OrderServiceLog
from core.serializers.order_service_log import OrderServiceLogSerializer


class OrderServiceLogListView(APIView):
    """
    Lista os logs de uma Ordem de Serviço específica.
    Ex: GET /api/v1/ordens-servico/<uuid:order_id>/logs/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(OrderService, pk=order_id)

        # Se quiser esconder OS deletadas logicamente, descomenta:
        # if order.is_deleted:
        #     return Response(
        #         {"detail": "Ordem de serviço não encontrada."},
        #         status=status.HTTP_404_NOT_FOUND,
        #     )

        logs = order.logs.all().select_related("changed_by").order_by("-changed_at")
        serializer = OrderServiceLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserOrderServiceLogListView(APIView):
    """
    Lista os logs de O.S. referentes a ações feitas pelo usuário autenticado.
    Ex: GET /api/v1/logs/minhas-acoes/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = (
            OrderServiceLog.objects
            .filter(changed_by=request.user)
            .select_related("order_service")
            .order_by("-changed_at")
        )
        serializer = OrderServiceLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
