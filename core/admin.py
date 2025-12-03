from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ServiceOrder

class CustomUserAdmin(UserAdmin):
    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj == request.user:
            return False
        return super().has_delete_permission(request, obj)

admin.site.register(User, CustomUserAdmin)

@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ('protocol', 'so_number', 'recipient_name', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('protocol', 'so_number', 'recipient_name', 'description')
