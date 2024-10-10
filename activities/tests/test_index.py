"""Module to test on index page of activities app."""
import django.test
from django import urls
from .shortcuts import create_activity, activity_to_json, create_test_user


class IndexTest(django.test.TestCase):
    """Test Cases for Index view."""

    def setUp(self):
        """Set up the common URL."""
        self.url = urls.reverse("activities:index")
        self.host_user = create_test_user("Host")

    def test_no_activity(self):
        """If no activities available, an appropriate messages is displayed."""
        response = self.client.get(self.url)
        self.assertJSONEqual(response.content, [])

    def test_future_activity(self):
        """Activities take places in future showed on the index page."""
        response, activity = create_activity(host=self.host_user)
        self.assertEqual(activity.people, 1)
        response = self.client.get(self.url)
        expected = [
            activity_to_json(activity)
        ]
        self.assertJSONEqual(response.content, expected)

    # def test_past_activity(self):
    #     """Activities take places in the past showed on the index page."""
    #     create_activity(host=self.host_user, days_delta=-1)
    #     response = self.client.get(urls.reverse("activities:index"))
    #     self.assertJSONEqual(response.content, [])

    # def test_future_and_past_activity(self):
    #     """Only activities take place in the future is showed on index page."""
    #     response, activity = create_activity(host=self.host_user)
    #     create_activity(host=self.host_user, days_delta=-1)
    #     response = self.client.get(urls.reverse("activities:index"))
    #     expected = [
    #         activity_to_json(activity)
    #     ]
    #     self.assertJSONEqual(response.content, expected)

    # def test_two_future_activity(self):
    #     """Both of activity is showed on index page."""
    #     response1, activity1 = create_activity(host=self.host_user)
    #     response2, activity2 = create_activity(host=self.host_user)
    #     response = self.client.get(urls.reverse("activities:index"))
    #     expected = [
    #         activity_to_json(activity1),
    #         activity_to_json(activity2)
    #     ]
    #     self.assertJSONEqual(response.content, expected)
