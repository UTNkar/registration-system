from django.db import models
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone

class CommonUserManager(UserManager):
    def get_by_natural_key(self, person_nr):
        return self.get(person_nr=person_nr)

    def create_user(self, person_nr, name, email, phone_nr, is_utn_member, password = None):
        """
        Creates a non-superuser identified by person_nr
        """
        now = timezone.now()
        if not person_nr:
            raise ValueError('The given person_nr must be set')
        email = UserManager.normalize_email(email)
        user = self.model(
            person_nr=person_nr,
            email=email,
            name=name,
            phone_nr=phone_nr,
            is_utn_member=is_utn_member,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login=now)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, person_nr, name, email, phone_nr, is_utn_member, password = None):
        """
        Creates a superuser identified by person_nr
        """
        now = timezone.now()
        if not person_nr:
            raise ValueError('The given person number must be set')
        email = UserManager.normalize_email(email)
        user = self.model(
            person_nr=person_nr,
            email=email,
            name=name,
            phone_nr=phone_nr,
            is_utn_member=is_utn_member,
            is_staff=True,
            is_active=True,
            is_superuser=True,
            last_login=now)

        user.set_password(password)
        user.save(using=self._db)
        return user

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
    status = models.CharField(max_length=20, choices=CHOICES)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=254, verbose_name='Name')
    email = models.EmailField(verbose_name='Email')
    password = models.CharField(max_length=254, verbose_name='Password')
    phone_nr = models.CharField(max_length=20, verbose_name='Phone number')
    person_nr = models.CharField(max_length=13, verbose_name='Person number', unique=True)
    is_utn_member = models.BooleanField(verbose_name='UTN Member')
    belongs_to_group = models.ForeignKey(
        "Group",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Group'
    )
    is_staff = models.BooleanField(verbose_name='Staff')
    is_active = models.BooleanField(verbose_name='Active')

    objects = CommonUserManager()

    USERNAME_FIELD = "person_nr"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name", "email", "phone_nr", "is_utn_member"]

    def __str__(self):
        return '{} ({})'.format(self.name, self.person_nr)

    def properties(self):
        pass

    class Meta():
        abstract = True


class User(AbstractUser):
    pass


class RiverraftingUser(User):
    LIFEVEST_SIZES = (
        ('XL', 'XL'),
        ('L', 'L'),
        ('M', 'M'),
        ('S', 'S'),
        ('XS', 'XS'),
    )
    lifevest_size = models.CharField(max_length = 2, choices=LIFEVEST_SIZES, verbose_name='Lifevest size')

    def properties(self):
        relevants = ['Name', 'Email', 'Phone number', 'Lifevest size']
        fields = get_user_model()._meta.fields
        return [ (field.verbose_name, getattr(self, field.name) ) for field in fields
                 if field.verbose_name in relevants ]


class AbstractGroup(models.Model):
    leader = models.ForeignKey("User",
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)

    name = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return '{}'.format(getattr(self, "name"))

    class Meta():
        abstract = True


class Group(AbstractGroup):
    pass


class RiverraftingGroup(Group):
    pass

admin.site.register(RiverraftingUser)
admin.site.register(RiverraftingGroup)
