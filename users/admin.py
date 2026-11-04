from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Role, User, Executor, Service, WorkingHours, TimeOff, Booking

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Роль", {"fields": ("role",)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Роль", {"fields": ("role",)}),
    )
    list_display = ("email", "username", "role", "is_staff",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)

class ServiceInline(TabularInline):
    model = Service
    extra = 0

class WorkingHoursInline(TabularInline):
    model = WorkingHours
    extra = 0

@admin.register(Executor)
class ExecutorAdmin(admin.ModelAdmin):
    inlines = [ServiceInline, WorkingHoursInline]
    list_display = ("user", "specialization",)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "executor", "duration_minutes", "price", "format", "is_active",)

@admin.register(TimeOff)
class TimeOffAdmin(admin.ModelAdmin):
    list_display = ("executor", "start", "end", "reason",)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("service", "user", "start", "end", "status",)
    list_filter = ("status",)
    readonly_fields = ("created_at",)
