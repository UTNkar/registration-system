from django.db import models
from ..common.abstract_group import AbstractGroup


class RiverRaftingTeam(AbstractGroup):
    name = models.CharField(
        max_length=254,
        blank=True,
        verbose_name='Team name'
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
