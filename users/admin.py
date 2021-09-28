from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from users.forms import AddNewUserForm
from . import models


class CustomUserAdmin(UserAdmin):
    add_form = AddNewUserForm
    search_fields = ('first_name', 'phone', 'email')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone', 'first_name',
                       'last_name', 'email', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',
                                         'phone', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        (_('Moisklad Data'), {'fields': ('moisklad_id',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(models.CustomUserModel)
class CustomUserModelAdmin(CustomUserAdmin):
    pass
