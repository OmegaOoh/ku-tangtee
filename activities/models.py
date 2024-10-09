"""Database Model for activities app."""
from typing import Any
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Activity(models.Model):
    """Activity model to store data of activity detail."""

    name = models.CharField(max_length=255)
    detail = models.CharField(max_length=1024)
    date = models.DateTimeField(default=timezone.now)
    max_people = models.IntegerField(null=True, blank=True)

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

    def host(self) -> User:
        """Return host of an activity."""
        return self.attend_set.filter(is_host=True)

    @property
    def people(self) -> int:
        """Return number of people attend this activity include host."""
        return self.attend_set.count()


class Attend(models.Model):
    """Attend model to store activity attendance."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    is_host = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Return user's first name and which activity they join."""
        return f"user {self.user.first_name} attend {self.activity.name}"

    def __repr__(self) -> str:
        """Return user's first name and which activity they join."""
        return str.__str__()
