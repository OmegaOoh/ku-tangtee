"""Module to test on detail page of activities app."""
import django.test
from activities.serializer.model_serializers import ActivitiesSerializer
from django import urls

from .shortcuts import activity_to_json, create_activity


class DetailTest(django.test.TestCase):
    """Test Cases for Detail View."""

    def test_past_activity(self):
        """Past activities should not be accessible."""
        _, activity = create_activity(days_delta=-1)
        response = self.client.get(urls.reverse("activities:detail", args=[activity.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, activity_to_json(activity))
        self.assertNotContains(response, activity.check_in_code)

    def test_future_activity(self):
        """Future/Upcoming activity should be accessible."""
        _, activity = create_activity(days_delta=1)
        response = self.client.get(urls.reverse("activities:detail", args=[activity.id]))

        self.assertJSONEqual(response.content, activity_to_json(activity))
        self.assertNotContains(response, activity.check_in_code)

    def test_with_max(self):
        """Maximum number of participant should be shown in detail page if it has been set."""
        data = {
            "name": "test_activity",
            "detail": "hello",
            "max_people": 10
        }
        _, activity = create_activity(data=data)
        response = self.client.get(urls.reverse("activities:detail", args=[activity.id]))
        expected = activity_to_json(activity)
        self.assertJSONEqual(response.content, expected)
