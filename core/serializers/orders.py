# core/serializers/orders.py
from rest_framework import serializers

from core.models import OrderService, OrderServiceLog
from core.services.sla_service import get_sla_status


class OrderServiceSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source="created_by.username")
    updated_by_username = serializers.ReadOnlyField(source="updated_by.username")

    status_display = serializers.CharField(source="get_status_display", read_only=True)
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    provider_display = serializers.CharField(source="get_provider_display", read_only=True)
    priority_display = serializers.CharField(source="get_priority_display", read_only=True)

    # campos extras de SLA para o frontend
    sla_status = serializers.SerializerMethodField()
    due_date = serializers.DateTimeField(source="sla_datetime", read_only=True)

    class Meta:
        model = OrderService
        fields = [
            "id",
            "protocol",
            "so_number",
            "type",
            "type_display",
            "status",
            "status_display",
            "recipient_name",
            "cpf",
            "provider",
            "provider_display",
            "priority",
            "priority_display",
            "description",
            "open_date",
            "sla_datetime",
            "due_date",
            "sla_status",
            "created_by",
            "created_by_username",
            "updated_by",
            "updated_by_username",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "open_date",
            "sla_datetime",
            "due_date",
            "sla_status",
            "created_by",
            "created_by_username",
            "updated_by",
            "updated_by_username",
            "created_at",
            "updated_at",
        ]

    def get_sla_status(self, obj: OrderService) -> str:
        return get_sla_status(obj)


class OrderServiceLogSerializer(serializers.ModelSerializer):
    changed_by_username = serializers.ReadOnlyField(source="changed_by.username")

    class Meta:
        model = OrderServiceLog
        fields = [
            "id",
            "change_type",
            "changed_at",
            "changed_by_username",
            "old_values",
            "new_values",
        ]
