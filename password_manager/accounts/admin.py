from django.contrib import admin
from .models import Accounts


class AccountsAdmin(admin.ModelAdmin):
    list_display = ('email', 'service_name', 'user')
    search_fields = ('email', 'service_name')
    list_filter = ('user',)


admin.site.register(Accounts, AccountsAdmin)
