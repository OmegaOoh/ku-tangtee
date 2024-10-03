"""Module to test on detail page of activities app."""
import django.test
from django import urls
from .shortcuts import create_activity


class DetailTest(django.test.TestCase):
    """Test Cases for Detail View."""
    
    def test_past_question(self):
        activity = create_activity("past", -1)
        response = self.client.get(urls.reverse("activities:detail", args=[activity.id]))
        self.assertEqual(response.status_code, 404)

    def test_future_question(self):
        activity = create_activity("past", 1)
        response = self.client.get(urls.reverse("activities:detail", args=[activity.id]))
        self.assertEqual(response.status_code, 200)

    def test_with_max(self):
        activity = create_activity("test1", 1, 1, 10)
        response = self.client.get(urls.reverse("activities:detail", args=[activity.id]))
        self.assertContains(response, f"/ {activity.max_people}")
