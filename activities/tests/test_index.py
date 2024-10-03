"""Module to test on index page of activities app."""
import django.test
from django import urls
from .shortcuts import create_activity


class IndexTest(django.test.TestCase):
    """Test Cases for Index view."""

    def test_no_activity(self):
        """If no activities available, an appropiate messages is displayed."""
        response = self.client.get(urls.reverse("activities:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Activity Available at the moment.")
        self.assertQuerySetEqual(response.context["activities"], [])

    def test_future_activity(self):
        """Activities take places in future showed on the index page."""
        activity = create_activity("future", 1)
        response = self.client.get(urls.reverse("activities:index"))
        self.assertQuerySetEqual(response.context["activities"], [activity])

    def test_past_activity(self):
        """Activities take places in the past showed on the index page."""
        create_activity("past", -1)
        response = self.client.get(urls.reverse("activities:index"))
        self.assertQuerySetEqual(response.context["activities"], [])

    def test_future_and_past_activity(self):
        """Only activities take place in the future is showed on index page."""
        activity = create_activity("future", 1)
        create_activity("past", -1)
        response = self.client.get(urls.reverse("activities:index"))
        self.assertQuerySetEqual(response.context["activities"], [activity])

    def test_two_future_activity(self):
        """Both of activity is showed on index page."""
        activity = create_activity("future", 1)
        activity2 = create_activity("future2", 2)
        response = self.client.get(urls.reverse("activities:index"))
        self.assertQuerySetEqual(response.context["activities"], [activity, activity2])
