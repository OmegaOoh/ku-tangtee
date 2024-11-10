"""Test for activity model of activities app."""
import django.test
from .shortcuts import create_activity, create_test_user, client_join_activity
from ..models import Attend


class TestActivityModel(django.test.TestCase):
    """TestCase Class for Activity model."""

    def test_can_join_equal_max(self):
        """can_join() return False as Number of people is equal to max_people."""
        data = {
            "name": "Exceed",
            "detail": "hello",
            "max_people": 1
        }
        _, activity = create_activity(data=data)
        self.assertTrue(activity.is_full())

    def test_str(self):
        """__str__ returns activity name."""
        data = {
            "name": "Fun activity",
            "detail": "This activity is fun"
        }
        _, activity = create_activity(data=data)
        self.assertEqual(str(activity), "Fun activity")

    def test_is_active_future(self):
        """is_active() return True if and only if the current time haven't surpassed the date."""
        _, activity = create_activity(days_delta=1)
        self.assertTrue(activity.is_active())

    def test_is_active_past(self):
        """is_active() return False if and only if the current time have surpassed the date."""
        _, activity = create_activity(days_delta=-1)
        self.assertFalse(activity.is_active())

    def test_can_join_less(self):
        """is_full() return False as Number of people is less than max_people."""
        data = {
            "name": "Less",
            "detail": "hello",
            "max_people": 10
        }
        _, activity = create_activity(data=data)
        self.assertFalse(activity.is_full())

    def test_can_join_past(self):
        """can_join return False when date is in the past."""
        _, activity = create_activity(days_delta=-1)
        self.assertFalse(activity.is_active())

    def test_can_join_future(self):
        """can_join return True when date is in the future."""
        _, activity = create_activity(days_delta=1)
        self.assertTrue(activity.is_active())

    def test_host(self):
        """Return user that is host of that activity."""
        host = create_test_user("My lovely host")
        _, activity = create_activity(host=host)
        self.assertEqual(activity.host(), [host])

    def test_participants(self):
        """Return participants list of the activity."""
        host = create_test_user("activity_host")
        _, activity = create_activity(host=host)
        user1 = create_test_user("Alexa")
        user2 = create_test_user("Bruce")
        user3 = create_test_user("Clark")
        for user in (user1, user2, user3):
            client_join_activity(self.client, user, activity)
        participants = activity.participants()
        self.assertEqual(participants, [user1, user2, user3])


class TestAttendModel(django.test.TestCase):
    """TestCase Class for Attend model."""

    def test_str(self):
        """__str__ returns attendance info."""
        data = {
            "name": "Fun activity",
            "detail": "This activity is fun"
        }
        _, activity = create_activity(data=data)
        attend_host = activity.attend_set.first()
        self.assertEqual(str(attend_host), "user host attend Fun activity")

        attendee = create_test_user("Alexa")
        client_join_activity(self.client, attendee, activity)
        attend_attendee = activity.attend_set.last()
        self.assertEqual(str(attend_attendee), "user Alexa attend Fun activity")

    def test_recently_joined(self):
        """Return a list of the latest 3 activities joined by a user, order by join time."""
        host = create_test_user("activity_host")
        _, activity1 = create_activity(host=host, data={"name": "act1", "detail": "act"})
        _, activity2 = create_activity(host=host, data={"name": "act2", "detail": "act"}, days_delta=2)
        _, activity3 = create_activity(host=host, data={"name": "act3", "detail": "act"})
        _, activity4 = create_activity(host=host, data={"name": "act4", "detail": "act"})

        attendee = create_test_user("Attend", rep_score=100)
        self.assertEqual(Attend.recently_joined(attendee), [])

        for activity in (activity1, activity2, activity3):
            client_join_activity(self.client, attendee, activity)
        self.assertEqual(Attend.recently_joined(attendee, 3), [activity3, activity2, activity1])

        client_join_activity(self.client, attendee, activity4)
        self.assertEqual(Attend.recently_joined(attendee, 3), [activity4, activity3, activity2])

    def test_active_joined_activity(self):
        """Return a list of active activities joined by a user and order by activity date."""
        host = create_test_user("activity_host")
        _, activity1 = create_activity(host=host, data={"name": "act1", "detail": "act"})
        _, activity2 = create_activity(host=host, data={"name": "act2", "detail": "act"}, days_delta=2)
        _, activity3 = create_activity(host=host, data={"name": "act3", "detail": "act"})
        _, activity4 = create_activity(host=host, data={"name": "act4", "detail": "act"})

        attendee = create_test_user("Attend", rep_score=100)
        self.assertEqual(Attend.active_joined_activity(attendee), [])

        for activity in (activity1, activity2, activity3):
            client_join_activity(self.client, attendee, activity)
        self.assertEqual(Attend.active_joined_activity(attendee), [activity1, activity3, activity2])

        client_join_activity(self.client, attendee, activity4)
        self.assertEqual(Attend.active_joined_activity(attendee), [activity1, activity3, activity4, activity2])
