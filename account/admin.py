from datetime import datetime, timedelta
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from rangefilter.filters import DateRangeQuickSelectListFilterBuilder

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

# @admin.register(NewPhone)
# class NewPhoneAdmin(admin.ModelAdmin):
#     list_display = ["id", "user", "phone", "secure_code", "created_at"]


# @admin.register(AuthSms)
# class SmsAdmin(admin.ModelAdmin):
#     list_display = ["id", "user", "secure_code", "created_at"]


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    readonly_fields = ["created_at"]
    list_display_links = ["id", "phone"]
    list_display = ["id", "phone", "first_name", "is_staff", "is_active"]
    search_fields = ["phone", "first_name"]
    ordering = ["phone"]
    list_filter = (
        ('is_staff'),
        ('is_active'),
        ("created_at", DateRangeQuickSelectListFilterBuilder(
            title="Kun bo'yichas salarash",
            default_start= datetime.now().replace(month=datetime.now().month),
            default_end=datetime.now()
        )),
    )
    fieldsets = (
        (None, {
            "fields": [
                "phone",
                "password",
                "first_name",
                "last_name",
                "created_at",
                "secure_code",
                "expiration_time",
                "new_phone_temp",
            ]
        }),
        ("Permissions", {
            "fields": [
                "is_staff",
                "is_active",
                "groups",
                "user_permissions"
            ]
        }),
    )
    # add_fieldsets = (
    #     (None, {
    #         "classes": ("wide",),
    #         "fields": (
    #             "phone", "password1", "password2", "first_name", "last_name", "is_staff",
    #             "is_active", "groups", "user_permissions"
    #         )}
    #     ),
    # )

