from django.db import models
from ..common import CommonUserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)


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
