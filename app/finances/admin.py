from django.contrib import admin

from app.finances.models import Finance


class FinanceAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "amount", "finance_status", "date_time")


admin.site.register(Finance, FinanceAdmin)

