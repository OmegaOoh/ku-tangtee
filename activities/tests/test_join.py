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
        self.url = urls.reverse("activities:create")
        self.host_user = create_test_user("Host")

    def test_join_with_get(self):
        """Join should return an error if user doesn't login."""
        data = {
            "name": "Can join",
            "detail": "This act can join",
            "max_people": 2
        }
        response = create_activity(
            client=self.client,
            host=self.host_user,
            days_delta=3,
            data=data
        )
        self.assertEqual(response.status_code, 200)
        response_dict = json.loads(response.content)

        new_act = models.Activity.objects.get(pk=int(response_dict["id"]))

        response = self.client.get(urls.reverse("activities:join", args=[new_act.id]))
        self.assertEqual(response.status_code, 405)

    def test_logout_join(self):
        """Jpin should respond with error if user are not authenticated."""
        data = {
            "name": "Can join",
            "detail": "This act can join",
            "max_people": 2
        }
        response = create_activity(
            client=self.client,
            host=self.host_user,
            days_delta=3,
            data=data
        )
        self.assertEqual(response.status_code, 200)
        response_dict = json.loads(response.content)

        new_act = models.Activity.objects.get(pk=int(response_dict["id"]))

        self.client.logout()
        response = self.client.post(urls.reverse("activities:join", args=[new_act.id]))
        self.assertEqual(response.status_code, 401)

    def test_join(self):
        """Join will increase number of people in activity."""
        data = {
            "name": "Can join",
            "detail": "This act can join",
            "max_people": 2
        }
        response = create_activity(
            client=self.client,
            host=self.host_user,
            days_delta=3,
            data=data
        )
        self.assertEqual(response.status_code, 200)
        response_dict = json.loads(response.content)

        new_act = models.Activity.objects.get(pk=int(response_dict["id"]))

        self.client.logout

        attender = create_test_user("Attend")
        self.client.force_login(attender)

        # activity = create_activity("Joinable", 2, 1)
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
        response = create_activity(
            client=self.client,
            host=self.host_user,
            days_delta=3,
            data=data
        )
        self.assertEqual(response.status_code, 200)
        response_dict = json.loads(response.content)

        new_act = models.Activity.objects.get(pk=int(response_dict["id"]))

        self.client.logout

        attender = create_test_user("Attend")
        self.client.force_login(attender)

        # activity = create_activity("Joinable", 2, 1)
        response = self.client.post(urls.reverse("activities:join", args=[new_act.id]))
        new_act.refresh_from_db()
        self.assertEqual(new_act.people, 1)
        self.assertJSONEqual(response.content, {"error": f"{new_act.name} is not joinable"})
