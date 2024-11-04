"""Database Model for profile app."""
from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.utils import timezone


class Profile(models.Model):
    """Profile model to store user's profile."""
    
    BASE_ACTIVITY_LIMIT = 3
    MAX_ACTIVITY_LIMIT = 10
    REP_SCORE_PER_1_LIMIT = 10

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=30, null=True, blank=True)
    pronoun = models.CharField(max_length=20, null=True, blank=True)
    ku_generation = models.PositiveSmallIntegerField()
    faculty = models.CharField(max_length=100,)
    major = models.CharField(max_length=100, null=True, blank=True)
    about_me = models.CharField(max_length=256, null=True, blank=True)
    
    # Reputation system related
    reputation_score = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(100)]
    )
    
    @property
    def active_activity_count(self) -> int:
        """Get number of active activity

        :return: Integer number indicate number of active activity that user currently join
        """
        
        # Filter only activity that still active and user is not a host.
        return int(self.user.attend_set.filter(
            activity__date__gte=timezone.now(), 
            is_host=False
        ).count()) 
    
    @property
    def join_limit(self) -> int:
        """Calculate user join limit base on user reputation score

        :return: Maximum number of activity that user able to join.
        """
        limit = self.BASE_ACTIVITY_LIMIT + (self.reputation_score // self.REP_SCORE_PER_1_LIMIT)
        return limit if limit < self.MAX_ACTIVITY_LIMIT else self.MAX_ACTIVITY_LIMIT
    
    @property
    def able_to_join_more(self) -> bool:
        return bool(self.active_activity_count < self.join_limit)
        
    def __str__(self) -> str:
        """Return user's username as string representative.

        :return: string containing user's username
        """
        return f"{self.user.username}'s profile"

    @classmethod
    def has_profile(cls, user: User) -> Any:
        """Check if the user has a profile.

        :return: true if the user has a profile, false otherwise
        """
        return cls.objects.filter(user__id=user.id).exists()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                name="User must have only 1 profile"
            )
        ]