"""Test for Join function."""
import django.test
from django import urls
from .shortcuts import create_activity


class JoinTest(django.test.TestCase):
    """Test Cases for join function."""

    def test_join_redirection(self):
        """Join redirect user to activity detail page."""
        activity = create_activity("Joinable", 1)
        response = self.client.post(urls.reverse("activities:join", args=[activity.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, urls.reverse("activities:detail", args=[activity.id]))

    def test_join(self):
        """Join will increase number of people in activity."""
        activity = create_activity("Joinable", 2, 1)
        self.client.post(urls.reverse("activities:join", args=[activity.id]))
        activity.refresh_from_db()
        self.assertEqual(activity.people, 2)

    def test_join_unjoinable(self):
        """Join will not increase number of people in activity as activities is full."""
        activity = create_activity("UnJoinable", 1, 10, 10)
        self.client.post(urls.reverse("activities:join", args=[activity.id]))
        self.assertEqual(activity.people, 10)
