"""Database Model for activities app."""
import string
import random
from typing import Any, Optional
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

CHECKIN_CODE_LEN = 6


def get_checkin_code() -> str:
    """Random 6 capital character.

    :return: string of random 6 character.
    """
    # choose from all lowercase letter
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(CHECKIN_CODE_LEN))
    return result_str


def get_end_registration_date() -> Any:
    """Get default end registration date.

    :return: default datetime of end registration date (5 days from now)
    """
    return timezone.now() + timezone.timedelta(days=5)


def get_end_date() -> Any:
    """Get default end date.

    :return: default datetime of end date (7 days from now)
    """
    return timezone.now() + timezone.timedelta(days=7)


class Locations(models.Model):
    """Location for activity."""

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)


class Activity(models.Model):
    """Activity model to store data of activity detail."""

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    detail = models.CharField(max_length=1024)
    on_site = models.BooleanField(default=False)
    locations = models.ForeignKey(Locations, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=get_end_date)
    end_registration_date = models.DateTimeField(default=get_end_registration_date)
    max_people = models.IntegerField(null=True, blank=True)
    check_in_allowed = models.BooleanField(default=False)
    check_in_code = models.CharField(max_length=6, null=True, default=None)
    minimum_reputation_score = models.SmallIntegerField(
        default=0,
        validators=[MaxValueValidator(100)]
    )
    is_cancelled = models.BooleanField(default=False)

    class Meta:
        """Meta Class of Activity Model."""
        
        unique_together = ['owner', 'name', 'detail', 'date', 'end_date']

    def update_check_in_code(self) -> str:
        """Regenerate activity check-in code."""
        self.check_in_code = get_checkin_code()
        self.save()
        return self.check_in_code

    def __str__(self) -> Any:
        """Return Activity Name as string representative.

        :return: activity name
        """
        return self.name

    def is_active(self) -> bool:
        """Check if activity is active.

        :return: True if activity is in joining period and not be cancelled.
        """
        return bool((self.end_registration_date >= timezone.now()) and not self.is_cancelled)

    def is_full(self) -> bool:
        """Check if max_people doesn't reach.

        :return: true if the activity is full, false otherwise
        """
        return False if (not self.max_people) or (self.people < self.max_people) else True

    def host(self) -> list[User]:
        """Find all user that is host of the activity (is_host is True), owner included.

        :return: list of hosts of the activity
        """
        return [a.user for a in self.attend_set.filter(is_host=True)]

    def is_hosts(self, user: User) -> bool:
        """Return boolean value which tell that are given user is host of the activity or not.

        :param user: User
        :return: True if the user is host of the activity, False otherwise
        """
        return user in self.host()

    def participants(self) -> list[User]:
        """Find all participants user of the activity (host excluded).

        :return: list of participants
        """
        return [a.user for a in self.attend_set.filter(is_host=False)]

    def user_status(self, user: User) -> dict[str, bool]:
        """Return dict contain status of user in each activity.

        :param user: User model instance
        :return: Dict contain user status in each activity.
        """
        if not self.is_participated(user):
            return {
                'is_joined': False,
                'is_checked_in': False
            }

        return {
            'is_joined': True,
            'is_checked_in': self.is_checked_in(user)
        }

    def is_participated(self, user: User) -> bool:
        """Return boolean value which tell that are given user are participate in activity or not.

        :param user: User model instance
        :return: Boolean value which tell user are participated in activity or not.
        """
        return bool(user in [a.user for a in self.attend_set.all()])

    def is_checked_in(self, user: User) -> bool:
        """Return boolean value which tell that are given user are already checked-in activity or not.

        :param user: User model instance
        :return: Boolean value which tell user are participated are already checked-in activity or not.
        """
        return bool(self.attend_set.get(user=user).checked_in)

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

    def rep_check(self, user: User) -> bool:
        """Verify that user reputation score meet minimum reputation score to join or not.

        :param user: User attempt to join an activity.
        :return: True is user reputation score meet mininum, otherwise false.
        """
        profile = user.profile_set.first()
        return bool(profile.reputation_score >= self.minimum_reputation_score)

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
                        is_host: Optional[bool] = False,
                        by_date: Optional[bool] = False) -> list[Activity]:
        """Class method that get recently joined activities of a user.

        :param user: the user to get activities for.
        :param records: the number of record needed for return
        :param is_host: if True, retrieve activities hosted by the user.
        :param by_date: on True, make result order in activity date instead of join time
        :return: The latest activities joined by a user, order by join time(default).
        """
        res = cls.objects.filter(user=user, is_host=is_host)
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
