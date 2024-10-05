"""Test for activity model of activities app."""
import django.test
from .shortcuts import create_activity


class TestActivityModel(django.test.TestCase):
    """TestCase Class for Activity model."""

    def test_can_join_equal_max(self):
        """can_join() return False as Number of people is equal to max_people."""
        activity = create_activity("Exceed", 1, 10, 10)
        self.assertFalse(activity.can_join())

    def test_can_join_less(self):
        """can_join() return True as Number of people is less than max_people."""
        activity = create_activity("Less", 1, 9, 10)
        self.assertTrue(activity.can_join())

    def test_can_join_past(self):
        """can_join return False when date is in the past."""
        activity = create_activity("Past", -1)
        self.assertFalse(activity.can_join())

    def test_can_join_future(self):
        """can_join return True when date is in the future."""
        activity = create_activity("Past", 1)
        self.assertTrue(activity.can_join())

    def test_upcoming(self):
        """Return True when activities took place in upcoming weeks."""
        activity = create_activity("upcoming", 7)
        self.assertTrue(activity.is_upcoming())
        activity = create_activity("not really upcoming", 8)
        self.assertFalse(activity.is_upcoming())
