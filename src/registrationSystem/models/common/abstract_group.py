from django.db import models
from django.contrib.auth import get_user_model


class AbstractGroup(models.Model):
    leader = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return '{}'.format(getattr(self, "name"))

    class Meta():
        abstract = True
