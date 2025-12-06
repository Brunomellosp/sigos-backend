# core/services/log_service.py
from typing import Any, Dict, Optional
from datetime import datetime, date
from uuid import UUID

from django.forms.models import model_to_dict

from core.models import OrderService, OrderServiceLog


def _serialize_value(value: Any):
    """
    Converte valores não serializáveis em JSON (datetime, date, UUID, etc.)
    para string.
    """
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    return value


def _serialize_instance(instance: OrderService) -> Dict[str, Any]:
    """
    Converte o model para dict e garante que todos os valores
    sejam serializáveis em JSON.
    """
    data = model_to_dict(instance)
    return {key: _serialize_value(value) for key, value in data.items()}


def create_order_log(
    order: OrderService,
    user,
    change_type: str,
    old_instance: Optional[OrderService] = None,
) -> None:
    old_data = _serialize_instance(old_instance) if old_instance else None
    new_data = _serialize_instance(order)

    OrderServiceLog.objects.create(
        order_service=order,
        changed_by=user,
        change_type=change_type,
        old_values=old_data,
        new_values=new_data,
    )
