from rest_framework import serializers
from core.models import OrderServiceLog
from core.serializers.users import UserSerializer  # você já tem esse serializer


class OrderServiceLogSerializer(serializers.ModelSerializer):
    changed_by = UserSerializer(read_only=True)

    class Meta:
        model = OrderServiceLog
        fields = [
            "id",
            "order_service",
            "changed_by",
            "changed_at",
            "change_type",
            "old_values",
            "new_values",
        ]
        read_only_fields = fields
