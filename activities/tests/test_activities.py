"""Test for activity model of activities app."""
import django.test
from .shortcuts import create_activity, create_test_user, client_join_activity


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
        self.assertFalse(activity.can_join())

    def test_can_join_less(self):
        """can_join() return True as Number of people is less than max_people."""
        data = {
            "name": "Less",
            "detail": "hello",
            "max_people": 10
        }
        _, activity = create_activity(data=data)
        self.assertTrue(activity.can_join())

    def test_can_join_past(self):
        """can_join return False when date is in the past."""
        _, activity = create_activity(days_delta=-1)
        self.assertFalse(activity.can_join())

    def test_can_join_future(self):
        """can_join return True when date is in the future."""
        _, activity = create_activity(days_delta=1)
        self.assertTrue(activity.can_join())

    def test_upcoming(self):
        """Return True when activities take place in upcoming weeks."""
        _, up_activity = create_activity(days_delta=7)
        self.assertTrue(up_activity.is_upcoming())

    def test_not_upcoming(self):
        """Return False when activities don't take place in upcoming weeks."""
        _, not_up_activity = create_activity(days_delta=8)
        self.assertFalse(not_up_activity.is_upcoming())

    def test_host(self):
        """Return user that is host of that activity."""
        host = create_test_user("My lovely host")
        _, activity = create_activity(host=host)
        self.assertEqual(activity.host(), host)

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
