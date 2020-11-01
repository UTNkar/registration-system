from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser

class AbstractSingletonModel(models.Model):
    """
    Taken from
    https://stackoverflow.com/questions/49735906/how-to-implement-singleton-in-django
    """
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Save object to the database. Removes all other entries if there
        are any.
        """
        self.__class__.objects.exclude(id=self.id).delete()
        super(AbstractSingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass
    
    @classmethod
    def load(cls):
        """
        Load object from the database. Failing that, create a new empty
        (default) instance of the object and return it (without saving it
        to the database).
        """
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


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
        ("accepted", "Accepted"),
        ("declined", "Declined")
    )

    name = models.CharField(max_length=254)
    email = models.EmailField()
    person_nr = models.CharField(max_length=13)
    is_utn_member = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=CHOICES)


class AbstractUser(AbstractBaseUser):
    name = models.CharField(max_length=254)
    email = models.EmailField()
    password = models.CharField(max_length=254)
    phone_nr = models.CharField(max_length=20)
    person_nr = models.CharField(max_length=13)
    is_utn_member = models.BooleanField(default=False)
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
