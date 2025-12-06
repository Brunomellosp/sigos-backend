from django.urls import path
from core.controllers.logs_controller import (
    OrderServiceLogListView,
    UserOrderServiceLogListView,
)

urlpatterns = [
    path(
        "ordens-servico/<uuid:order_id>/logs/",
        OrderServiceLogListView.as_view(),
        name="order-service-logs",
    ),
    path(
        "logs/minhas-acoes/",
        UserOrderServiceLogListView.as_view(),
        name="user-order-service-logs",
    ),
]
