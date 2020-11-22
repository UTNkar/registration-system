from django.db import models
from ..common.abstract_singleton_model import AbstractSingletonModel


class RiverRaftingCost(AbstractSingletonModel):
    lifevest = models.IntegerField()
    wetsuit = models.IntegerField()
    helmet = models.IntegerField()
    raft_fee = models.IntegerField()
