from django.db import models


class ImportantDate(models.Model):
    """
    Important event dates.
    
    An important date is dates on which events or deadlines happen.

    'On the 14th of february there will be a raffle pub.'
    'On the 1st of March payment closes.'
    And so on.
    """
    date = models.DateField(verbose_name="Date")
    desc = models.CharField(max_length=254, verbose_name="Description")

    def __str__(self):
        return '{} - {}'.format(getattr(self, "date"), getattr(self, "desc"))

