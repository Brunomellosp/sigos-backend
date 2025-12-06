from django.urls import path
from core.controllers.order_service_controller import (
    OrderServiceListCreateView,
    OrderServiceDetailView,
    OrderServiceLogsView,
)
from core.controllers.csv_import_controller import OrderServiceCSVImportView

urlpatterns = [
    path("", OrderServiceListCreateView.as_view(), name="orders-list-create"),
    path("<uuid:id>/", OrderServiceDetailView.as_view(), name="orders-detail"),
    path("<uuid:id>/logs/", OrderServiceLogsView.as_view(), name="orders-logs"),
    path("importar-csv/", OrderServiceCSVImportView.as_view(), name="orders-import-csv"),
]
