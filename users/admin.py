from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Client, CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_superuser', 'is_staff', 'role']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Client)
