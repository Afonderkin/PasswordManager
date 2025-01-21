from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'is_staff')
    search_fields = ('username',)

    list_filter = ('is_staff', 'is_superuser', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
