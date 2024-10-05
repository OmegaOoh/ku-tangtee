"""Database Model for activities app."""
from typing import Any
from django.db import models
from django.utils import timezone


class Activity(models.Model):
    """Activity model to store data of activity detail."""

    name = models.CharField(max_length=255)
    detail = models.CharField(max_length=1024)
    date = models.DateTimeField(default=timezone.now)
    max_people = models.IntegerField(null=True, blank=True)
    people = models.IntegerField(default=0)

    def __str__(self) -> models.CharField:
        """Return Activity Name as string representative."""
        return self.name

    def can_join(self) -> Any:
        """Return True if max_people doesn't reached and date doesn't past, Otherwise false."""
        if self.max_people:
            return self.date >= timezone.now() and self.people < self.max_people
        else:
            return self.date >= timezone.now()

    def is_upcoming(self) -> Any:
        """Return True if activities took place on incoming weeks, Otherwise false."""
        return timezone.now() + timezone.timedelta(weeks=1) >= self.date and self.can_join()
