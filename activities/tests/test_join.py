"""Test for Join function."""
import django.test
from django import urls
from .shortcuts import create_activity, create_test_user
from activities import models
import json


class JoinTest(django.test.TestCase):
    """Test Cases for join function."""

    def setUp(self):
        """Set up the common URL."""
        self.url = urls.reverse("activities:index")
        # self.host_user = create_test_user("Host")

    def test_join_with_get(self):
        """Join should return an error if user doesn't log in."""
        _, new_act = create_activity()

        response = self.client.get(urls.reverse("activities:join", args=[new_act.id]))
        self.assertEqual(response.status_code, 405)

    def test_logout_join(self):
        """Join should respond with error if user are not authenticated."""
        _, new_act = create_activity()

        self.client.logout()
        response = self.client.post(urls.reverse("activities:join", args=[new_act.id]))
        self.assertEqual(response.status_code, 401)

    def test_join(self):
        """Join will increase number of people in activity."""
        _, new_act = create_activity()

        attender = create_test_user("Attend")
        self.client.force_login(attender)

        self.assertEqual(new_act.people, 1)

        response = self.client.post(urls.reverse("activities:join", args=[new_act.id]))
        new_act.refresh_from_db()
        self.assertEqual(new_act.people, 2)
        self.assertJSONEqual(response.content, {"message": f"You successfully joined {new_act.name}"})

    def test_join_full(self):
        """Join will not increase number of people in activity as activities is full."""
        data = {
            "name": "Unjoinable",
            "detail": "This act is unjoinable",
            "max_people": 1
        }
        response, new_act = create_activity(data=data)
        self.assertEqual(response.status_code, 200)

        attender = create_test_user("Attend")
        self.client.force_login(attender)

        response = self.client.post(urls.reverse("activities:join", args=[new_act.id]))
        new_act.refresh_from_db()
        self.assertEqual(new_act.people, 1)
        self.assertJSONEqual(response.content, {"error": f"{new_act.name} is not joinable"})

    def test_rejoin_joined_activity(self):
        """Cannot join activity that already joined."""
        _, new_act = create_activity()

        attender = create_test_user("Attend")
        self.client.force_login(attender)

        # First time joined, number of people increase.
        response = self.client.post(urls.reverse("activities:join", args=[new_act.id]))
        new_act.refresh_from_db()
        self.assertEqual(new_act.people, 2)

        # Second time joined, get error and number of people stays the same.
        response = self.client.post(urls.reverse("activities:join", args=[new_act.id]))
        new_act.refresh_from_db()
        self.assertEqual(new_act.people, 2)
        self.assertJSONEqual(response.content, {"error": f"You've already joined {new_act.name}"})
