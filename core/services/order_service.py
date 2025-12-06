# core/services/order_service.py

from typing import Any, Dict
from copy import deepcopy

from django.db import transaction

from core.models import OrderService
from core.services.log_service import create_order_log
from core.services.sla_service import calculate_sla


def create_order(data: Dict[str, Any], user) -> OrderService:
    with transaction.atomic():
        order = OrderService(**data)
        order.created_by = user
        calculate_sla(order)
        order.save()
        create_order_log(order, user, change_type="CREATED")
        return order


def update_order(order: OrderService, data: Dict[str, Any], user) -> OrderService:
    old_instance = deepcopy(order)

    for key, value in data.items():
        setattr(order, key, value)

    # se tiver o campo updated_by no modelo:
    # order.updated_by = user

    calculate_sla(order)

    with transaction.atomic():
        order.save()
        create_order_log(
            order,
            user,
            change_type="UPDATED",
            old_instance=old_instance,
        )
    return order


def soft_delete_order(order: OrderService, user) -> None:
    old_instance = deepcopy(order)

    with transaction.atomic():
        # se seu modelo tiver is_deleted:
        # order.is_deleted = True
        # order.save()
        # senão, delete físico:
        order.delete()

        create_order_log(
            order,
            user,
            change_type="DELETED",
            old_instance=old_instance,
        )
