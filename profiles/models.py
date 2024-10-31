"""Database Model for profile app."""
from datetime import datetime
from typing import Any
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    """Profile model to store user's profile."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=30, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    pronoun = models.CharField(max_length=20, null=True, blank=True)
    ku_generation = models.PositiveSmallIntegerField(null=True, blank=True)
    faculty = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    about_me = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self) -> str:
        """Return user's username as string representative.

        :return: string containing user's username
        """
        return f"{self.user.username}'s profile"

    @property
    def age(self) -> Any:
        """Calculate age of the user by subtracting birthday.

        :return: age of the user
        """
        today = datetime.today().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    @classmethod
    def has_profile(cls, user: User) -> Any:
        """Check if the user has a profile.

        :return: true if the user has a profile, false otherwise
        """
        return cls.objects.filter(user__id=user.id).exists()
