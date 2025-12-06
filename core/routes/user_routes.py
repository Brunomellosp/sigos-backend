# core/routes/user_routes.py
from django.urls import path
from core.controllers.user_controller import UserListCreateView, UserDetailView

urlpatterns = [
    path("", UserListCreateView.as_view(), name="users-list-create"),
    path("<uuid:pk>/", UserDetailView.as_view(), name="users-detail"),
]
