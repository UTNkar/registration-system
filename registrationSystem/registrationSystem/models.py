import uuid
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser


class InterestCheck(models.Model):
    """Interest checks start out as unconfirmed, and once the mail has
    been confirmed, the Interest check is considered active and
    "waiting" to receive a spot.

    Once a raffle has been held, a "waiting" interest check is moved
    to either the lost or won states. Those who have won can then
    decide to accept their spot and move into the "accepted" state, or
    decline and move to the "declined" state.

    If a new raffle is held, those who have "lost" can choose to move back
    into the "waiting" state to join another round of the raffle.

    Similarly, if a new raffle is executed while there are still
    interest checks in the "won" state (whom has not accepted or
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
    status = models.CharField(max_length=20, choices=CHOICES)


class AbstractUser(AbstractBaseUser):
    name = models.CharField(max_length=254)
    email = models.EmailField()
    password = models.CharField(max_length=254)
    phone_nr = models.CharField(max_length=20)
    person_nr = models.CharField(max_length=13)
    is_utn_member = models.BooleanField()
    belongs_to_group = models.ForeignKey(
        "Group",
        on_delete=models.SET_NULL,
        null=True
    )

    USERNAME_FIELD = "person_nr"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name", "email", "phone_nr", "is_utn_member"]

    def __str__(self):
        return '{} ({})'.format(self.name, self.person_nr)

    class Meta():
        abstract = True


class User(AbstractUser):
    pass


class RiverraftingUser(User):
    pass


class AbstractGroup(models.Model):
    leader = models.ForeignKey("User",
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)

    name = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.leader.name, )

    class Meta():
        abstract = True


class Group(AbstractGroup):
    pass


class RiverraftingGroup(Group):
    pass


admin.site.register(RiverraftingUser)
admin.site.register(RiverraftingGroup)


class EmailConfirmations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    interestCheckId = models.ForeignKey(
        "InterestCheck", on_delete=models.CASCADE
        )
