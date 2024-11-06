"""Database Model for activities app."""
from typing import Any, Optional
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def get_end_registration_date() -> Any:
    """Get default end registration date."""
    return timezone.now() + timezone.timedelta(days=5)


def get_end_date() -> Any:
    """Get default end date."""
    return timezone.now() + timezone.timedelta(days=7)


class Activity(models.Model):
    """Activity model to store data of activity detail."""

    name = models.CharField(max_length=255)
    detail = models.CharField(max_length=1024)
    date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=get_end_date)
    end_registration_date = models.DateTimeField(default=get_end_registration_date)
    max_people = models.IntegerField(null=True, blank=True)
    check_in_allowed = models.BooleanField(default=False)
    check_in_code = models.CharField(max_length=6, null=True, default=None)

    def __str__(self) -> Any:
        """Return Activity Name as string representative.

        :return: activity name
        """
        return self.name

    def is_active(self) -> Any:
        """Check if activity is active.

        :return: True if activity is in joining period.
        """
        return self.end_registration_date >= timezone.now()

    def can_join(self) -> Any:
        """Check if max_people doesn't reach and date doesn't past.

        :return: true if the activity is join able, false otherwise
        """
        return self.is_active() and (not self.max_people or self.people < self.max_people)

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

    def is_participated(self, user: User) -> Any:
        """Return boolean value which tell that are given user are participate in activity or not.

        :param user: _description_
        :return: _description_
        """
        return user in self.participants()

    def is_checkin_period(self) -> Any:
        """Return boolean value which tell that are given user can check-in in activity or not.

        :return: True if user can still check-in in this activity, False otherwise.
        """
        return (timezone.now() > self.date) and (timezone.now() < self.end_date)

    def verified_check_in_code(self, attempt: str) -> Any:
        """Verify that given check-in code are match actual check-in code or not.

        :param attempt: Given check-in code to verify.
        :return: True if given check-in code match actual check-in code
                False if check-in code are not created yet or given check-in code are not match.
        """
        if not (self.check_in_code):
            return False

        return self.check_in_code == attempt

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
    checked_in = models.BooleanField(default=False)
    rep_decrease = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Return activity attendance information.

        :return: user's username and the activity they've joined
        """
        return f"user {self.user.username} attend {self.activity.name}"

    @classmethod
    def recently_joined(cls, user: User,
                        records: Optional[int | None] = None,
                        by_date: Optional[bool] = False) -> list[Activity]:
        """Class method that get recently joined activities of a user.

        :param user: the user to get activities for.
        :param records: the number of record needed for return
        :param by_date: on True, make result order in activity date instead of join time
        :return: The latest activities joined by a user, order by join time(default).
        """
        res = cls.objects.filter(user=user)
        # Ordering
        if by_date:
            res = res.order_by('-activity__date')
        else:
            res = res.order_by('-id')

        if records:
            res = res[:records]
        return [a.activity for a in res]

    @classmethod
    def active_joined_activity(cls, user: User) -> list[Activity]:
        """Class method that get all active activity that a user have joined.

        :param user: the user to get activities for.
        :return: Active activities joined by a user and order by activity date.
        """
        return [a.activity for a in
                cls.objects.filter(user=user, activity__date__gte=timezone.now()).order_by("activity__date")]


class Attachment(models.Model):
    """Image attachment for activity."""

    image = models.ImageField('Activity', upload_to="activities/", height_field=None, width_field=None, max_length=None)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
