"""Module to test on detail page of activities app."""
import json
import django.test
from django import urls
from .shortcuts import create_activity, activity_to_json


class DetailTest(django.test.TestCase):
    """Test Cases for Detail View."""

    def test_past_activity(self):
        """Past activities should not be accessible."""
        activity = create_activity("past", -1)
        response = self.client.get(urls.reverse("activities:detail", args=[activity.id]))
        self.assertEqual(response.status_code, 404)

    def test_future_activity(self):
        """Future/Upcoming activity should be accessible."""
        activity = create_activity("past", 1)
        response = self.client.get(urls.reverse("activities:detail", args=[activity.id]))
        self.assertJSONEqual(response.content, activity_to_json(activity, True))

    def test_with_max(self):
        """Maximum number of participant should be shown in detail page if it has been set."""
        activity = create_activity("test1", 1, 1, 10)
        response = self.client.get(urls.reverse("activities:detail", args=[activity.id]))
        self.assertJSONEqual(response.content, activity_to_json(activity, True))
