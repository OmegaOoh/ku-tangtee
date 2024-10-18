"""Module to test on detail page of activities app."""
import json
import django.test
from django import urls
from .shortcuts import create_activity


class DetailTest(django.test.TestCase):
    """Test Cases for Detail View."""

    def test_past_activity(self):
        """Past activities should not be accessible."""
        _, activity = create_activity(days_delta=-1)
        response = self.client.get(urls.reverse("activities:detail", args=[activity.id]))
        self.assertEqual(response.status_code, 404)

    def test_future_activity(self):
        """Future/Upcoming activity should be accessible."""
        _, activity = create_activity(days_delta=1)
        response = self.client.get(urls.reverse("activities:detail", args=[activity.id]))
        content = json.loads(response.content)
        self.assertEqual(content['name'], activity.name)
        self.assertEqual(content['detail'], activity.detail)
        self.assertEqual(content['max_people'], activity.max_people)
        self.assertEqual(len(content['people']), activity.people)

    def test_with_max(self):
        """Maximum number of participant should be shown in detail page if it has been set."""
        data = {
            "name": "test_activity",
            "detail": "",
            "max_people": 10
        }
        _, activity = create_activity(data=data)
        response = self.client.get(urls.reverse("activities:detail", args=[activity.id]))
        content = json.loads(response.content)
        self.assertEqual(content['name'], activity.name)
        self.assertEqual(content['detail'], activity.detail)
        self.assertEqual(content['max_people'], activity.max_people)
        self.assertEqual(len(content['people']), activity.people)
