import uuid
from django.db import models


class EmailConfirmation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    raffleEntryId = models.ForeignKey(
        "RaffleEntry", on_delete=models.CASCADE
    )
