from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from core.models import OrderService
from core.services.sla_service import get_sla_status


def get_overview():
    qs = OrderService.objects.filter(is_deleted=False)
    total = qs.count()

    by_status = qs.values("status").annotate(total=Count("id"))

    now = timezone.now()
    in_24h = 0
    in_48h = 0
    late = 0

    for order in qs:
        status = get_sla_status(order)
        if status == "late":
            late += 1
        elif order.sla_datetime:
            delta = order.sla_datetime - now
            if delta <= timedelta(hours=24):
                in_24h += 1
            elif delta <= timedelta(hours=48):
                in_48h += 1

    return {
        "total_orders": total,
        "by_status": list(by_status),
        "sla": {
            "due_in_24h": in_24h,
            "due_in_48h": in_48h,
            "late": late,
        },
    }
