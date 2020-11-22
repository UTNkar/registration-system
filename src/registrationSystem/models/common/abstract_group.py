from django.contrib.auth import get_user_model
from django.db import models


class AbstractGroup(models.Model):
    leader = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    def get_group_members(self):
        group_members = get_user_model().objects.filter(
            belongs_to_group=self.leader.belongs_to_group
        )

        return group_members

    def get_non_none_fields(self, attribute):
        """

        """
        group_members = self.get_group_members()
        non_none_fields = group_members.exclude(
            **{attribute: None}
        )

        return non_none_fields

    def __str__(self):
        return '{}'.format(getattr(self, "name"))

    class Meta():
        abstract = True
