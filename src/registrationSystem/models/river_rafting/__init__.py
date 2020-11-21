# flake8: noqa
from django.conf import settings
from django.contrib import admin

from .river_rafting_raffle_state import RiverRaftingRaffleState
from .river_rafting_user import RiverRaftingUser
from .river_rafting_team import RiverRaftingTeam
from .raffle_entry import RaffleEntry
from .email_confirmation import EmailConfirmation

if settings.EVENT == 'RIVERRAFTING':
    admin.site.register(RiverRaftingUser)
    admin.site.register(RiverRaftingTeam)
