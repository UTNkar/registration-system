from django.contrib import admin
from registrationSystem.models import RiverRaftingUser, RaffleEntry, RiverRaftingRaffleState
from django.utils.html import format_html
from django.urls import reverse, path
from django.conf.urls import url
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

@admin.register(RiverRaftingRaffleState)
class RiverRaftingRaffleStateAdmin(admin.ModelAdmin):
    list_display = ["state"]
    # Raffle system
    change_list_template = "admin/riverraftingrafflestate/riverraftingrafflestate_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('update/', self.update)
        ]
        return new_urls + urls

    def update(self, request):
        raffle = RiverRaftingRaffleState.load()
        if "open_button" in request.POST and raffle.state == "closed":
            raffle.state = "open"
            raffle.save()
            return HttpResponseRedirect("../")
        elif "close_button" in request.POST:
            raffle.state = "closed"
            raffle.save()
            return HttpResponseRedirect("../")
        
        return HttpResponseRedirect("../")
        

@admin.register(RaffleEntry)
class RaffleEntryAdmin(admin.ModelAdmin):
    list_display = ["name", "status", "is_utn_member"]
    ordering = ["name"]
    actions = ["set_raffle_status_won", "set_raffle_status_lost"]

    def set_raffle_status_won(modeladmin, request, queryset):
        queryset.update(status="won")
    set_raffle_status_won.short_description = "Set selected status to 'won'"

    def set_raffle_status_lost(modeladmin, request, queryset):
        queryset.update(status="lost")
    set_raffle_status_lost.short_description = "Set selected status to 'lost'"


    # Raffle system
    change_list_template = "admin/raffleentry/raffleentry_changelist.html"
    
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
        return super(RaffleEntryAdmin, self).changelist_view(request, extra_context=extra_context)
