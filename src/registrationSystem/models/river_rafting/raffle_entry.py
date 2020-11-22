from django.db import models


class RaffleEntry(models.Model):
    """
    Raffle entries start out as unconfirmed, and once the mail has
    been confirmed, the raffle entry is considered active and
    "waiting" to receive a spot.

    Once a raffle has been held, a "waiting" raffle entry is moved to
    either the lost or won states. Those who have won can then decide
    to accept their spot and move into the "accepted" state, or
    decline and move to the "declined" state.

    If a new raffle is held, those who have "lost" can choose to move
    back into the "waiting" state to join another round of the raffle.

    Similarly, if a new raffle is executed while there are still
    raffle entries in the "won" state (whom has not accepted or
    declined yet), they are moved to the lost state and are allowed to
    join the raffle again by transitioning to the "waiting" state,
    should they choose to.

    """

    CHOICES = (
        ("mail unconfirmed", "Mail-Unconfirmed"),
        ("waiting", "Waiting"),
        ("won", "Won"),
        ("lost", "Lost"),
        ("declined", "Declined"),
        ("accepted", "Accepted"),
        ("confirmed", "Confirmed")
    )

    name = models.CharField(max_length=254)
    email = models.EmailField()
    person_nr = models.CharField(max_length=13)

    is_utn_member = models.BooleanField(default=False)
    status = models.CharField(max_length=20,
                              choices=CHOICES,
                              default=CHOICES[0][0])

    class Meta:
        verbose_name = "Raffle Entry"
        verbose_name_plural = "Raffle entries"
