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

    def __str__(self) -> Any:
        """Return Activity Name as string representative.

        :return: activity name
        """
        return self.name

    def is_active(self) -> bool:
        """Check if activity is active.

        :return: True if activity is active.
        """
        return self.date >= timezone.now()

    def can_join(self) -> Any:
        """Check if max_people doesn't reach and date doesn't past.

        :return: true if the activity is join able, false otherwise
        """
        return self.is_active() and (not self.max_people or self.people < self.max_people)

    def is_upcoming(self) -> Any:
        """Check if activities took place on incoming weeks.

        :return: true if the activity took place on incoming weeks, false otherwise
        """
        return timezone.now() + timezone.timedelta(weeks=1) >= self.date and self.can_join()

    def host(self) -> User:
        """Find user that is host of the activity (is_host is True).

        :return: the host of the activity
        """
        return self.attend_set.filter(is_host=True).first().user

    def participants(self) -> list[User]:
        """Find all participants user of the activity (host excluded).

        :return: list of participants
        """
        return [a.user for a in self.attend_set.filter(is_host=False)]

    @property
    def people(self) -> int:
        """Count number of Attend objects for the activity (host included).

        :return: number of people attend the activity
        """
        return int(self.attend_set.count())


class Attend(models.Model):
    """Attend model to store activity attendance."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    is_host = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Return activity attendance information.

        :return: user's username and the activity they've joined
        """
        return f"user {self.user.username} attend {self.activity.name}"

    def __repr__(self) -> str:
        """Return activity attendance information.

        :return: user's username and the activity they've joined
        """
        return self.__str__()
