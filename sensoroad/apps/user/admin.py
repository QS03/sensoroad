from django.contrib import admin
from django.contrib.auth import admin as auth_admin

# Register your models here.
from .models import User


class SensoryUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['id', 'username', 'member_type', 'city', 'state']
    search_fields = ('city', 'state')


admin.site.register(User)