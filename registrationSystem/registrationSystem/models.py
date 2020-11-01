import uuid
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser


class InterestCheck(models.Model):
    """
    Interest checks start out as unconfirmed, and once
    the mail has been confirmed checks progress in to the confirmed status.

    Once a raffle has been held, an interest check can enter either the
    lost or won states. Those who have won are done; those who have lost
    can reapply and then enter the reapplying state.

    Those who reapply can also win or lose. Reapplicants who win enter the
    pending state, where they can win once they claim their spot.

    Reapplicants who lose can reapply again, repeating the cycle.

    Those pending can also become declined, stopping them from further
    reapplying.
    """

    CHOICES = (
        ("mail unconfirmed", "Mail-Unconfirmed"),
        ("mail confirmed", "Mail-Confirmed"),
        ("won", "Won"),
        ("lost", "Lost"),
        ("reapplying", "Reapplying"),
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


class EmailConfirmations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    interestCheckId = models.ForeignKey(
        "InterestCheck", on_delete=models.CASCADE
        )
