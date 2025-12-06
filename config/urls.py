from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("core.routes.auth_routes")),
    path("api/v1/ordens-servico/", include("core.routes.order_routes")),
    path("api/v1/users/", include("core.routes.user_routes")),
    path("api/v1/dashboard/", include("core.routes.dashboard_routes")),
    path("api/v1/logs", include("core.routes.log_routes")),
]
