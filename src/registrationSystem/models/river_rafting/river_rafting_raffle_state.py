from django.db import models
from ..common.abstract_singleton_model import AbstractSingletonModel


class RiverRaftingRaffleState(AbstractSingletonModel):
    """The raffle state holds the state for the current raffle. The
    raffle can be:
    Open: The raffle is open and lost applicants can choose to join
    Drawn: The raffle has been drawn and winners can accept or
    decline their spot
    Closed: The raffle is closed, winners that have not accepted are
    moved into the lost state and losers cannot apply for another
    round until the raffle opens again
    """
    class Meta:
        verbose_name = 'The River Rafting Raffle'
        verbose_name_plural = 'The River Rafting Raffle'

    CHOICES = (
        ("open", "Open"),
        ("drawn", "Drawn"),
        ("closed", "Closed")
    )
    state = models.CharField(max_length=20, choices=CHOICES)
