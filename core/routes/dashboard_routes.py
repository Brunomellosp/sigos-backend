from django.urls import path
from core.controllers.dashboard_controller import DashboardOverviewView

urlpatterns = [
    path("overview/", DashboardOverviewView.as_view(), name="dashboard-overview"),
]
