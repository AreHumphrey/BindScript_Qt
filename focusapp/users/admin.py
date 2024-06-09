from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Add any additional configuration for the admin interface here

admin.site.register(CustomUser, CustomUserAdmin)