from django.db import models
from ..common.abstract_singleton_model import AbstractSingletonModel


class RiverRaftingCost(AbstractSingletonModel):
    lifevest = models.IntegerField(verbose_name="Lifevest (kr)")
    wetsuit = models.IntegerField(verbose_name="Wetsuit (kr)")
    helmet = models.IntegerField(verbose_name="Helmet (kr)")
    raft_fee = models.IntegerField(verbose_name="Raft fee (kr)")

    def __str__(self):
        return "River rafting costs"
