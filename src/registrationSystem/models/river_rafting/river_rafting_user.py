from django.db import models
from ..common.abstract_user import AbstractUser


class RiverRaftingUser(AbstractUser):
    LIFEVEST_SIZES = (
        ('XL', 'XL'),
        ('L', 'L'),
        ('M', 'M'),
        ('S', 'S'),
        ('XS', 'XS'),
    )

    WETSUIT_SIZES = (
        ('L', 'L'),
        ('M', 'M'),
        ('S', 'S'),
    )

    # Kolla med FORSKÅ
    HELMET_SIZES = (
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

    wetsuite_size = models.CharField(
        max_length=2,
        choices=WETSUIT_SIZES,
        verbose_name='Wetsuit size',
        blank=True,
        null=True
    )

    helmet_size = models.CharField(
        max_length=2,
        choices=HELMET_SIZES,
        verbose_name='Helmet size',
        blank=True,
        null=True
    )

    belongs_to_group = models.ForeignKey(
        "RiverraftingTeam",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Group'
    )
