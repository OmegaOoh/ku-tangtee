"""Module on test activity editing."""
import json
import django.test
from datetime import datetime
from django import urls
from activities import models
from .shortcuts import activity_to_json, time_formatter, create_activity, create_test_user, put_request_json_data
from django.utils import timezone


class EditActivityTest(django.test.TestCase):
    """Test case for editing activity."""

    def setUp(self):
        """Set up the common URL and create an activity."""
        data = {
            "name": "Test Activity",
            "detail": "This is a test activity"
        }
        self.host = create_test_user("host")
        _, self.activity = create_activity(host=self.host, data=data)

        self.client.force_login(self.host)

        # Set the URL to the detail page
        self.url = urls.reverse("activities:detail", args=[self.activity.id])

    def test_valid_activity_editing(self):
        """Edit should return a success message with the updated activity name."""
        data = {
            "name": "Updated Activity",
            "detail": "This is an updated activity",
            "max_people": 50,
        }
        # Send PUT request with new activity data
        response = put_request_json_data(self.url, self.client, data)
        response_dict = json.loads(response.content)
        updated_act = models.Activity.objects.get(pk=self.activity.id)
        updated_act_json = activity_to_json(updated_act)
        # Compare the serialized activity with the expected data
        self.assertEqual(updated_act_json['name'], data['name'])
        self.assertEqual(updated_act_json['detail'], data['detail'])
        self.assertEqual(updated_act_json['max_people'], data['max_people'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict["message"], f"You have successfully edited the activity {data.get('name')}")

    def test_valid_activity_editing_date(self):
        """Edit should return a success message with the updated activity date."""
        data = {
            "name": "Updated Activity",
            "detail": "Detail of updated activity",
            "date": "2024-10-10T10:20:00.000Z",
            "max_people": 200,
            "people": 20,
        }
        # Send PUT request with new activity data
        response = put_request_json_data(self.url, self.client, data)
        response_dict = json.loads(response.content)
        updated_act = models.Activity.objects.get(pk=self.activity.id)
        updated_act_json = activity_to_json(updated_act)
        activity_date = time_formatter(data['date'])
        # Compare the serialized activity with the expected data
        self.assertEqual(updated_act_json['date'], activity_date)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict["message"], f"You have successfully edited the activity {data.get('name')}")

    def test_invalid_activity_editing_with_too_long_activity_name(self):
        """Editing should return json with error message."""
        data = {
            "name": "This is too long" * 50,
            "detail": "This is invalid activity",
            "date": "2024/10-10T10:20:00.00Z",
            "max_people": 10,
        }
        response = put_request_json_data(self.url, self.client, data)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'date': [
            'Datetime has wrong format. Use one of these formats instead: '
            'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'],
            'name': ['Ensure this field has no more than 255 characters.']})

    def test_non_host_edit_activity(self):
        """Edit should return error message when the editor isn't host."""
        hacker = create_test_user("not_host")
        self.client.force_login(hacker)

        response = put_request_json_data(self.url, self.client, {})
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'message': 'User must be the host to perform this action.'})

    def test_invalid_activity_editing_with_people_exceed_capacity(self):
        """Editing should be rollbacked."""
        user1 = create_test_user("Participant number 1")
        self.client.force_login(user=user1)
        self.assertEqual(self.activity.people, 1)
        response = self.client.post(urls.reverse("activities:detail", args=[self.activity.id]))
        self.activity.refresh_from_db()
        self.assertEqual(self.activity.people, 2)
        response_dict = response.json()
        self.assertEqual(response_dict['message'], f'You have successfully joined the activity {self.activity.name}')
        data = {
            "name": "Updated Activity",
            "detail": "This is should be failed",
            "max_people": 1,
        }
        original_data = {
            "name": "Test Activity",
            "detail": "This is a test activity",
            "max_people": None,
        }
        self.client.force_login(user=self.host)
        response = put_request_json_data(self.url, self.client, data)
        response_dict = json.loads(response.content)
        updated_act = models.Activity.objects.get(pk=self.activity.id)
        updated_act_json = activity_to_json(updated_act)
        # The updated activity should be the same as original one
        self.assertEqual(updated_act_json['name'], original_data['name'])
        self.assertEqual(updated_act_json['detail'], original_data['detail'])
        self.assertEqual(updated_act_json['max_people'], original_data['max_people'])
        self.assertEqual(response_dict["message"], "Number of participants exceed the capacity.")
