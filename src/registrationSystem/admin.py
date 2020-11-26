from django.contrib import admin
from django.conf import settings
from django.urls import path
from registrationSystem.models import (
    RaffleEntry,
    RiverRaftingRaffleState,
    RiverRaftingUser,
    RiverRaftingTeam,
    RiverRaftingCost,
    ImportantDate,
)

from registrationSystem.forms import RiverRaftingUserForm

from django.http import HttpResponseRedirect
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class RiverRaftingRaffleStateAdmin(admin.ModelAdmin):
    list_display = ["state"]
    # Raffle system
    change_list_template = (
        "admin/riverraftingrafflestate/riverraftingrafflestate_changelist.html"
    )

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
        elif "close_button" in request.POST:
            raffle.state = "closed"
            raffle.save()

        return HttpResponseRedirect("../")


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
        # TODO: Implement actual raffle logic.
        # params = request.POST
        # desired_utn_member_percentage = params["utn-member-percentage"]
        self.model.objects.all().update(status="won")
        self.message_user(request, "Randomized winners!")
        return HttpResponseRedirect("../")

    # Add useful stats to admin view
    def changelist_view(self, request, extra_context=None):
        utn_count = self.model.objects.filter(is_utn_member=True).count()
        all_count = self.model.objects.all().count()
        percentage = (utn_count / all_count) * 100 if all_count != 0 else 0
        extra_context = extra_context or {}
        extra_context['utn_percentage'] = "{:.0f}".format(percentage)
        return super(RaffleEntryAdmin, self).changelist_view(
            request,
            extra_context=extra_context
        )

class RiverRaftingUserAdmin(BaseUserAdmin):
    list_display = ["name", "person_nr", "email"]
    list_filter = ["name", "person_nr", "email"]
    ordering = ["name", "person_nr", "email"]

    fieldsets = (
        (None, {'fields': ('name', 'email',
                           'person_nr', 'phone_nr',
                           'password', 'is_utn_member',
                           'is_staff', 'lifevest_size',
                           'wetsuite_size', 'helmet_size',
                           'belongs_to_group',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('name', 'email',
                           'person_nr', 'phone_nr',
                           'password', 'is_utn_member',
                           'is_staff', 'lifevest_size',
                           'wetsuite_size', 'helmet_size',
                           'belongs_to_group')}),
    )


if settings.EVENT == 'RIVERRAFTING':
    admin.site.register(RaffleEntry, RaffleEntryAdmin)
    admin.site.register(RiverRaftingRaffleState, RiverRaftingRaffleStateAdmin)
    admin.site.register(RiverRaftingUser, RiverRaftingUserAdmin)
    admin.site.register(RiverRaftingTeam)
    admin.site.register(RiverRaftingCost)

admin.site.register(ImportantDate)
