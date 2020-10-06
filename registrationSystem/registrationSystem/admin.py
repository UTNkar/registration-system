from django.contrib import admin
from registrationSystem.models import InterestCheck


@admin.register(InterestCheck)
class RaffleAdmin(admin.ModelAdmin):
    list_display = ["name", "status"]
    ordering = ["name"]
    actions = ["set_raffle_status_won", "set_raffle_status_lost"]

    def set_raffle_status_won(modeladmin, request, queryset):
        queryset.update(status="won")
    set_raffle_status_won.short_description = "Set selected status to 'won'"

    def set_raffle_status_lost(modeladmin, request, queryset):
        queryset.update(status="lost")
    set_raffle_status_lost.short_description = "Set selected status to 'lost'"
