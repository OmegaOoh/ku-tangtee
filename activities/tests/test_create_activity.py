"""Module to test on activity creation."""
import json
import django.test
from datetime import datetime
from django import urls
from django.utils import timezone
from activities import models
from .shortcuts import post_request_json_data, activity_to_json, create_activity, create_test_user


class CreateActivityTest(django.test.TestCase):
    """Test case for creating activity."""

    def setUp(self):
        """Set up the common URL."""
        self.url = urls.reverse("activities:create")
        self.host_user = create_test_user("Host")

    def test_get_request(self):
        """Create should return error message when got a GET request."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)

    def test_valid_activity_creation_without_max_people(self):
        """Create should return message with successful message and activity name."""
        data = {
            "name": "Valid Activity",
            "detail": "This is valid activity",
        }
        response, new_act = create_activity(
            client=self.client,
            host=self.host_user,
            days_delta=3,
            data=data
        )
        response_dict = json.loads(response.content)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response_dict["message"], f"Your have successfully create activity {data.get('name')}")
        self.assertEqual(new_act.name, data.get('name'))
        self.assertEqual(new_act.people, 1)

    def test_valid_activity_creation_with_max_people(self):
        """Create should return message with successful message and activity name."""
        data = {
            "name": "Valid Activity",
            "detail": "This is valid activity",
            "max_people": 10
        }

        response, new_act = create_activity(
            client=self.client,
            host=self.host_user,
            data=data
        )
        response_dict = json.loads(response.content)

        # Check Response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict["message"], f"Your have successfully create activity {data.get('name')}")
        # Check Activity Object
        self.assertEqual(new_act.name, data.get('name'))
        self.assertEqual(new_act.people, 1)
        self.assertEqual(new_act.max_people, data.get("max_people"))

    def test_invalid_activity_creation_without_name(self):
        """Create should return error with error message."""
        data = {
            "detail": "This is invalid activity",
            "max_people": 10
        }

        response, activity = create_activity(
            client=self.client,
            host=self.host_user,
            data=data
        )

        response_dict = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Error occur", response_dict["error"])

    def test_invalid_activity_creation_with_wrong_date_format(self):
        """Create should return json with error message."""
        data = {
            "name": "Wrong date format",
            "detail": "This is invalid activity",
            "date": "2024/10-10T1",
            "max_people": 10
        }
        self.client.force_login(self.host_user)
        response = post_request_json_data(self.url, self.client, data)
        self.assertEqual(response.status_code, 400)

        response_dict = json.loads(response.content)
        self.assertIn("Error occur", response_dict["error"])

    def test_invalid_activity_creation_with_too_long_activity_name(self):
        """Create should return json with error message."""
        data = {
            "name": "This is too long" * 50,
            "detail": "This is invalid activity",
            "max_people": 10
        }
        response, activity = create_activity(
            client=self.client,
            host=self.host_user,
            data=data
        )
        self.assertEqual(response.status_code, 400)

        response_dict = json.loads(response.content)
        self.assertIn("Error occur", response_dict["error"])
