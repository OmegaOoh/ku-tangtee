"""Database Model for profile app."""
from typing import Any
from django.db import models
from django.db.models import Q
from activities.models import Activity, Attend
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.utils import timezone


class Profile(models.Model):
    """Profile model to store user's profile."""

    BASE_ACTIVITY_LIMIT = 3
    MAX_ACTIVITY_LIMIT = 10
    REP_SCORE_PER_1_LIMIT = 10
    CHECK_IN_REPUTATION_INCREASE = 1
    CHECK_IN_REPUTATION_DECREASE = 1

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
        """Get number of active activity.

        :return: Integer number indicate number of active activity that user currently join
        """
        # Filter only activity that still active and user is not a host.
        return int(self.user.attend_set.filter(
            activity__date__gte=timezone.now(),
            is_host=False
        ).count())

    @property
    def join_limit(self) -> Any:
        """Calculate user join limit base on user reputation score.

        :return: Maximum number of activity that user able to join.
        """
        limit = self.BASE_ACTIVITY_LIMIT + (self.reputation_score // self.REP_SCORE_PER_1_LIMIT)
        return min(self.MAX_ACTIVITY_LIMIT, limit)

    @property
    def able_to_join_more(self) -> bool:
        """Return boolean determine that user can join more activity or not."""
        return bool(self.active_activity_count < self.join_limit)

    def __str__(self) -> str:
        """Return user's username as string representative.

        :return: string containing user's username
        """
        return f"{self.user.username}'s profile"

    def decrease_reputation(self, attend: Attend) -> None:
        """Decrease reputation score when user misses a check-in and mark that reputation is already decreased."""
        if not attend.rep_decrease:
            self.reputation_score -= self.CHECK_IN_REPUTATION_DECREASE
            self.reputation_score = max(0, self.reputation_score)
            self.save(update_fields=['reputation_score'])
            attend.rep_decrease = True
            attend.save(update_fields=['rep_decrease'])

    def increase_reputation(self) -> None:
        """Increase reputation score after user check-in."""
        self.reputation_score += self.CHECK_IN_REPUTATION_INCREASE
        self.reputation_score = min(100, self.reputation_score)
        self.save(update_fields=['reputation_score'])

    @classmethod
    def check_missed_check_ins(cls) -> None:
        """Check for check-in status for the ended activities.

        Check for users who missed check-ins and decrease their reputation.
        Check if there is at least an attendee who check-in, if not, decrease hosts reputation.
        Also decrease hosts reputation when the activity is cancelled.
        """
        now = timezone.now()
        activities = Activity.objects.filter(Q(end_date__lt=now) | Q(is_cancelled=True))

        for activity in activities:
            attendees = activity.attend_set.filter(is_host=False)
            hosts = activity.attend_set.filter(is_host=True)

            # deduct attendee point when not check-in
            if not activity.is_cancelled:
                for attendee in attendees:
                    profile = cls.objects.get(user=attendee.user)
                    if not attendee.checked_in and not attendee.rep_decrease:
                        profile.decrease_reputation(attendee)

            # deduct host point when no attendee check-in or the activity is cancelled
            if (attendees.filter(checked_in=True).count() <= 0 < attendees.count()) or activity.is_cancelled:
                for host in hosts:
                    profile = cls.objects.get(user=host.user)
                    profile.decrease_reputation(host)

    @classmethod
    def has_profile(cls, user: User) -> Any:
        """Check if the user has a profile.

        :return: true if the user has a profile, false otherwise
        """
        return cls.objects.filter(user__id=user.id).exists()

    class Meta:
        """Meta class for creating Profile."""

        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                name="User must have only 1 profile"
            )
        ]
