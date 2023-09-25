from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("phone", "first_name", "is_staff", "is_active",)
    list_filter = ("phone", "first_name", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("phone", "password", "first_name", "last_name",)}),
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
    search_fields = ("phone",)
    ordering = ("phone",)
