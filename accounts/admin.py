from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User
from .form import UserCreationForm

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    fieldsets = (
            (None, {'fields': ('username', 'email', 'password')}),
            (_('Personal info'), {'fields': (
                'first_name', 'last_name', 'phone_number', 'role', 'line'
            )}),
            (_('Permissions'), {'fields': (
                'is_active', 'is_staff', 'is_superuser', 
                'groups', 'user_permissions')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'role', 'email', 'password1')}
        ),
    )

admin.site.register(User, UserAdmin)
