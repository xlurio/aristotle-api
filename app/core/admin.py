from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import forms
from core import models


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("registry", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("registry", "password1", "password2"),
            },
        ),
    )
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm
    list_display = ("registry", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("registry", "first_name", "last_name")
    ordering = ("registry",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(models.User, UserAdmin)
