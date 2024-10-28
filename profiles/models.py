"""Database Model for profile app."""
from typing import Any
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    """Profile model to store user's profile."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=30, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    religion = models.CharField(max_length=100, null=True, blank=True)
    is_single = models.BooleanField(null=True, blank=True)
    student_id = models.IntegerField(null=True, blank=True)
    generation = models.PositiveSmallIntegerField(null=True, blank=True)
    faculty = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    tel = models.CharField(max_length=10, null=True, blank=True)
    contact = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=1024)

    def __str__(self) -> str:
        """Return ???.

        :return: ???
        """
        return f"user {self.user.username}'s profile"
