from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser


class InterestCheck(models.Model):
    """
    Interest checks start out as 'mail unconfirmed', and once
    the mail has been confirmed, they progress to "In the raffle".

    Once the first raffle has been held, an interest check, with status
    "In the raffle" can enter either the lost or won states.
    Those who have won will receive an email and create an account.
    Those who have lost can reapply during the second raffle and then
    enter "In the raffle" once again.

    During the second raffle, interest checks that are selected in the raffle
    enter the pending state. If the person claims their spot their status
    is set to won. If the person does not claim their spot their status is set
    to declined, stopping them from applying again.

    The second raffle can also be reseted. All interest checks
    that are in the state "In the raffle" are then set to "must reapply". If
    a person wants to be a part of the raffle again they have to reapply
    and will then enter the state "In the raffle" once again.

    When a person who has received a spot and has created an account, the
    status of their interest check is set to confirmed so that the
    administrators knows that the person has accepted their spot.
    """

    CHOICES = (
        ("mail unconfirmed", "Mail-Unconfirmed"),
        ("in the raffle", "In the raffle"),
        ("confirmed", "Confirmed"),
        ("won", "Won"),
        ("lost", "Lost"),
        ("must reapply", "Must reapply"),
        ("pending", "Pending"),
        ("declined", "Declined")
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
