from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import Group
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from .models import Category, Expense, Banks


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    def delete_admin_logs(self, request, queryset):
        queryset.delete()

        self.message_user(
            request,
            ngettext(
                "%d log was successfully deleted.",
                "%d logs were successfully deleted.",
                len(queryset),
            ) % int(len(queryset)),
            messages.SUCCESS,
        )

    delete_admin_logs.short_description = (
        "Delete the selected ADMIN Logs without sticking")

    actions = [delete_admin_logs]


admin.site.unregister(Group)

admin.site.site_header = admin.site.site_title = "Finance Management System"

@admin.register(Banks)
class BanksAdmin(admin.ModelAdmin):
    search_fields = list_display = (
        "name",
        "amount_deposited",
        "amount_threshold",
    )
    list_per_page = 10

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = list_display = ("name", "color")
    list_per_page = 10

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    search_fields = list_display = ("date", "category", "description", "amount", "repeat_next_month", "bank")
    list_filter = ("date", "category", "repeat_next_month", "bank")
    list_per_page = 50