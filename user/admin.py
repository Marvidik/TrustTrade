from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": (
                "phone_number",
                "country_code",
                "language_preference",
                "is_verified",
                "trust_score",
            )
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
