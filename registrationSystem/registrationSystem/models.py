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
    personnr = models.CharField(max_length=13)
    status = models.CharField(max_length=20, choices=CHOICES)


class AbstractUser(AbstractBaseUser):
    namn = models.CharField(max_length=254)
    mail = models.EmailField()
    password = models.CharField(max_length=254)
    # TODO: These are not showing up when creating
    # a user through the admin interface.
    # Investigate if the fields exist in the database.
    phone_nr = models.CharField(max_length=20)
    personnr = models.CharField(max_length=13)
    is_utn_member = models.BooleanField()
    belongs_to_group = models.ForeignKey(
        "Group",
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta():
        abstract = True


class User(AbstractUser):
    pass


class RiverraftingUser(User):
    pass


class AbstractGroup(models.Model):
    leader = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=254, blank=True)

    class Meta():
        abstract = True


class Group(AbstractGroup):
    pass


class RiverraftingGroup(Group):
    pass


admin.site.register(RiverraftingUser)
admin.site.register(RiverraftingGroup)
