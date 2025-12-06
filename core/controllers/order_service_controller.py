from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from core.models import OrderService
from core.serializers.orders import OrderServiceSerializer, OrderServiceLogSerializer
from core.services.order_service import create_order, update_order, soft_delete_order


class OrderServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderServiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "type", "priority", "recipient_name"]
    search_fields = ["so_number", "recipient_name", "provider", "description"]
    ordering_fields = ["open_date", "sla_datetime", "priority"]

    def get_queryset(self):
        qs = OrderService.objects.filter(is_deleted=False)
        data_inicio = self.request.query_params.get("data_inicio")
        data_fim = self.request.query_params.get("data_fim")
        if data_inicio:
            qs = qs.filter(open_date__date__gte=data_inicio)
        if data_fim:
            qs = qs.filter(open_date__date__lte=data_fim)
        return qs

    def perform_create(self, serializer):
        data = serializer.validated_data
        order = create_order(data, self.request.user)
        serializer.instance = order


class OrderServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderServiceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return OrderService.objects.filter(is_deleted=False)

    def perform_update(self, serializer):
        order = self.get_object()
        data = serializer.validated_data
        updated_order = update_order(order, data, self.request.user)
        serializer.instance = updated_order

    def perform_destroy(self, instance):
        soft_delete_order(instance, self.request.user)


class OrderServiceLogsView(generics.ListAPIView):
    serializer_class = OrderServiceLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs["id"]
        return OrderService.objects.get(pk=order_id).logs.all()
