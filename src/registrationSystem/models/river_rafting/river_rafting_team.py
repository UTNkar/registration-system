from django.db import models
from ..common.abstract_group import AbstractGroup
from coolname import generate


def get_cool_team_name():
    return " ".join(x.capitalize() for x in generate(2)) + "s"


class RiverRaftingTeam(AbstractGroup):

    max_team_members = 4

    name = models.CharField(
        max_length=254,
        verbose_name='Team name',
        default=get_cool_team_name,
    )

    number = models.IntegerField(
        verbose_name='Start Number',
        null=True,
        blank=True
    )

    environment_raft = models.BooleanField(
        verbose_name='I want an environmentally friendly raft',
        default=False
    )

    presentation = models.CharField(
        max_length=250,
        verbose_name='Presentation',
        null=True,
        blank=True
    )

    payment_initialized = models.BooleanField(
        verbose_name="Payment initialized",
        default=False
    )

    def get_number_of_lifevests(self):
        members_with_lifevests = \
            super().get_group_members_where_nonempty("lifevest_size")

        return len(members_with_lifevests)

    def get_number_of_wetsuits(self):
        members_with_wetsuits = \
            super().get_group_members_where_nonempty("wetsuite_size")

        return len(members_with_wetsuits)

    def get_number_of_helmets(self):
        members_with_helmets = \
            super().get_group_members_where_nonempty("helmet_size")

        return len(members_with_helmets)
