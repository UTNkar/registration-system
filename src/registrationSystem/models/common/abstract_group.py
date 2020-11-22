import uuid
from django.contrib.auth import get_user_model
from django.db import models


class AbstractGroup(models.Model):
    leader = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    join_id = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return '{}'.format(getattr(self, "name"))

    class Meta():
        abstract = True
