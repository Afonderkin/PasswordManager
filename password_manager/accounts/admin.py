from django.contrib import admin
from .models import Accounts


class AccountsAdmin(admin.ModelAdmin):
    list_display = ('email', 'service_name', 'user', 'created_at', 'updated_at')
    search_fields = ('email', 'service_name')
    list_filter = ('user',)


admin.site.register(Accounts, AccountsAdmin)
