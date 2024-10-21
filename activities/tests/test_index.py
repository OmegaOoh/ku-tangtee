"""Module to test on index page of activities app."""
import django.test
from django import urls
from .shortcuts import create_activity, activity_to_json, create_test_user
import json


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

    def test_past_activity(self):
        """Activities take places in the past showed on the index page."""
        create_activity(host=self.host_user, days_delta=-1)
        response = self.client.get(urls.reverse("activities:index"))
        self.assertJSONEqual(response.content, [])

    def test_future_and_past_activity(self):
        """Only activities take place in the future is showed on index page."""
        _, activity = create_activity(host=self.host_user)
        create_activity(host=self.host_user, days_delta=-1)
        response = self.client.get(urls.reverse("activities:index"))
        expected = [
            activity_to_json(activity)
        ]
        self.assertJSONEqual(response.content, expected)

    def test_two_future_activity(self):
        """Both of activity is showed on index page."""
        _, activity1 = create_activity(host=self.host_user)
        _, activity2 = create_activity(host=self.host_user)
        response = self.client.get(urls.reverse("activities:index"))
        expected = [
            activity_to_json(activity1),
            activity_to_json(activity2)
        ]
        self.assertJSONEqual(response.content, expected)

    def test_search_by_keyword(self):
        """Only activities with keyword in its name showed on index page."""
        _, activity1 = create_activity(host=self.host_user, data={"name": "tes1", "detail": "12"})
        _, activity2 = create_activity(host=self.host_user, data={"name": "test2", "detail": "tes1"})
        _, activity3 = create_activity(host=self.host_user, data={"name": "12", "detail": "test2"})

        json_act1 = activity_to_json(activity1)
        json_act2 = activity_to_json(activity2)
        json_act3 = activity_to_json(activity3)

        response = self.client.get(urls.reverse("activities:index") + "?keyword=test")
        self.assertJSONEqual(response.content, [json_act2])

        response = self.client.get(urls.reverse("activities:index") + "?keyword=tes")
        self.assertJSONEqual(response.content, [json_act1, json_act2])

        response = self.client.get(urls.reverse("activities:index") + "?keyword=1")
        self.assertJSONEqual(response.content, [json_act1, json_act3])

        response = self.client.get(urls.reverse("activities:index") + "?keyword=")
        self.assertJSONEqual(response.content, [json_act1, json_act2, json_act3])

        response = self.client.get(urls.reverse("activities:index") + "?keyword=Engarde")
        self.assertJSONEqual(response.content, [])
