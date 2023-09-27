from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, AuthSms


@admin.register(AuthSms)
class SmsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "secure_code", "created_at"]


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    readonly_fields = ["created_at"]
    list_display_links = ["id", "phone"]
    list_display = ["id", "phone", "first_name", "is_staff", "is_active"]
    list_filter = ["phone", "first_name", "is_staff", "is_active"]
    fieldsets = (
        (None, {"fields": ("phone", "password", "first_name", "last_name", "created_at")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone", "password1", "password2", "first_name", "last_name", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ["phone"]
    ordering = ["phone"]
