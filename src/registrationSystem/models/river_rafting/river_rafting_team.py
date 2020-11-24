from django.db import models
from ..common.abstract_group import AbstractGroup
from coolname import generate


class RiverRaftingTeam(AbstractGroup):

    max_team_members = 4

    name = models.CharField(
        max_length=254,
        verbose_name='Team name',
        default=(" ".join(x.capitalize() for x in generate(2)) + "s")
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
