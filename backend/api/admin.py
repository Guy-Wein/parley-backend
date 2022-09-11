from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Transaction, User, Advance
# Register your models here.

""" class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'bank_account'
        ) """

admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Advance)
