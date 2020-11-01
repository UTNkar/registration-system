from django.contrib import admin
from registrationSystem.models import InterestCheck
from django.utils.html import format_html
from django.urls import reverse, path
from django.conf.urls import url
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

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


    # Raffle system
    change_list_template = "admin/interestcheck/interestcheck_changelist.html"
    
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('raffle/', self.make_raffle)
        ]
        return new_urls + urls

    def make_raffle(self, request):
        params = request.POST;
        desired_utn_member_percentage = params["utn-member-percentage"]
        
        # TODO: Implement actual raffle logic.
        self.model.objects.all().update(status="won")
        self.message_user(request, "Randomized winners!")
        return HttpResponseRedirect("../")

    # Add useful stats to admin view
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['utn_percentage'] = "{:.0f}".format(
            self.model.objects.filter(is_utn_member=True).count() / self.model.objects.all().count() * 100
        )
        return super(RaffleAdmin, self).changelist_view(request, extra_context=extra_context)