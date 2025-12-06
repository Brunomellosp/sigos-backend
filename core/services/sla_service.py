# core/services/sla_service.py
from datetime import timedelta

from django.utils import timezone

from core.models import OrderService, ServiceOrderPriority


def calculate_sla(order: OrderService) -> None:
    """
    Preenche order.sla_datetime com base na prioridade.
    """
    base_datetime = getattr(order, "open_date", None) or timezone.now()

    if order.priority == ServiceOrderPriority.CRITICAL:
        delta = timedelta(hours=4)
    elif order.priority == ServiceOrderPriority.HIGH:
        delta = timedelta(hours=24)
    elif order.priority == ServiceOrderPriority.MEDIUM:
        delta = timedelta(hours=48)
    else:  # LOW ou qualquer outro valor
        delta = timedelta(hours=72)

    order.sla_datetime = base_datetime + delta


def get_sla_status(order: OrderService) -> str:
    """
    Retorna o status do SLA para uso no dashboard / frontend:

    - 'overdue'          -> já passou do prazo
    - 'nearing_due_date' -> faltam <= 24h para vencer
    - 'on_time'          -> ainda no prazo
    """
    if not order.sla_datetime:
        return "on_time"

    now = timezone.now()

    if order.sla_datetime < now:
        return "overdue"

    if order.sla_datetime - now <= timedelta(hours=24):
        return "nearing_due_date"

    return "on_time"
