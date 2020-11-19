import uuid
from django.db import models
from django.contrib import admin
from django.conf import settings


from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

from .common import CommonUserManager

class AbstractUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=254, verbose_name='Name')
    email = models.EmailField(verbose_name='Email')
    password = models.CharField(max_length=254, verbose_name='Password')
    phone_nr = models.CharField(max_length=20, verbose_name='Phone number')
    person_nr = models.CharField(
        max_length=13, verbose_name='Person number', unique=True
    )
    is_utn_member = models.BooleanField(verbose_name='UTN Member')
    is_staff = models.BooleanField()
    objects = CommonUserManager()

    USERNAME_FIELD = "person_nr"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name", "email", "phone_nr", "is_utn_member"]

    def __str__(self):
        return '{} ({})'.format(self.name, self.person_nr)

    class Meta():
        abstract = True

        
class RiverraftingUser(AbstractUser):
    LIFEVEST_SIZES = (
        ('XL', 'XL'),
        ('L', 'L'),
        ('M', 'M'),
        ('S', 'S'),
        ('XS', 'XS'),
    )

    lifevest_size = models.CharField(
        max_length=2,
        choices=LIFEVEST_SIZES,
        verbose_name='Lifevest size'
    )

    belongs_to_group = models.ForeignKey(
        "RiverraftingTeam",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Group'
    )


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


class RiverraftingTeam(AbstractGroup):
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
        verbose_name='I want an environmentally friendly raft'
    )

    presentation = models.CharField(
        max_length=250,
        verbose_name='Presentation',
        null=True,
        blank=True
    )


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

    is_utn_member = models.BooleanField(default=False)
    status = models.CharField(max_length=20,
                              choices=CHOICES,
                              default=CHOICES[0][0])




class EmailConfirmations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    interestCheckId = models.ForeignKey(
        "InterestCheck", on_delete=models.CASCADE
    )


class ImportantDate(models.Model):
    date = models.DateField()

if settings.EVENT == 'RIVERRAFTING':
    admin.site.register(RiverraftingUser)
    admin.site.register(RiverraftingTeam)


