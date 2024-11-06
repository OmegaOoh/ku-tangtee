"""Module on test activity owner access granting and removing."""
import json
import django.test
from django import urls
from .shortcuts import client_join_activity, create_activity, create_test_user, put_request_json_data, activity_to_json
from .. import models


class GrantRemoveHostTest(django.test.TestCase):
    """Test case for granting and removing host access for activity."""

    def setUp(self):
        """Set up the common URL and create an activity."""
        data = {
            "name": "Test Activity",
            "detail": "This is a test activity",
        }
        self.owner = create_test_user("owner")
        _, self.activity = create_activity(host=self.owner, data=data)

        self.user = create_test_user("user")

        self.participant = create_test_user("participant")
        client_join_activity(client=self.client, user=self.participant, activity=self.activity)

        self.client.force_login(self.owner)

        # Set the URL to the detail page
        self.url = urls.reverse("activities:detail", args=[self.activity.id,])

        self.attend = lambda user: self.activity.attend_set.filter(user=user).first()

        self.grant = lambda user: put_request_json_data(self.url, self.client, {"grant_host": [user.id]})
        self.remove = lambda user: put_request_json_data(self.url, self.client, {"remove_host": [user.id]})

    def test_grant_and_remove_host(self):
        """Return a success message and user gain and lose host access for activity accordingly."""
        self.assertEqual(self.activity.host(), [self.owner])

        # Send PUT request for grant
        response = self.grant(self.participant)
        response_dict = json.loads(response.content)
        self.assertEqual(self.activity.host(), [self.owner, self.participant])
        self.assertTrue(self.attend(self.participant).checked_in)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict["message"], f"You have successfully edited the activity {self.activity.name}")

        # Send PUT request for remove
        response = self.remove(self.participant)
        response_dict = json.loads(response.content)
        self.assertEqual(self.activity.host(), [self.owner])
        self.assertFalse(self.attend(self.participant).checked_in)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict["message"], f"You have successfully edited the activity {self.activity.name}")

    def test_co_host_activity_editing(self):
        """Co-host should be able to edit activity."""
        self.grant(self.participant)
        self.client.force_login(self.participant)

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

    def test_remove_host(self):
        """Return a success message and user host access for activity is removed."""
        response = self.remove(self.participant)
        response_dict = json.loads(response.content)
        self.assertEqual(self.activity.host(), [self.owner])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict["message"], f"You have successfully edited the activity {self.activity.name}")

    def test_grant_host_for_non_participants(self):
        """Return an error message when grant host for non-participants."""
        response = self.grant(self.user)
        response_dict = json.loads(response.content)
        self.assertEqual(self.activity.host(), [self.owner])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_dict["message"], f"Cannot find user {self.user.username} in this activity.")

    def test_remove_host_for_non_participants(self):
        """Return an error message when remove host for non-participants."""
        response = self.remove(self.user)
        response_dict = json.loads(response.content)
        self.assertEqual(self.activity.host(), [self.owner])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_dict["message"], f"Cannot find user {self.user.username} in this activity.")

    def test_grant_host_owner(self):
        """Return an error message when grant host for owner."""
        response = self.grant(self.owner)
        response_dict = json.loads(response.content)
        self.assertEqual(self.activity.host(), [self.owner])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_dict["message"], 'Cannot modify access of your own activity.')

    def test_remove_host_owner(self):
        """Return an error message when remove host for owner."""
        response = self.remove(self.owner)
        response_dict = json.loads(response.content)
        self.assertEqual(self.activity.host(), [self.owner])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_dict["message"], "Cannot modify access of your own activity.")

    def test_not_owner(self):
        """Return an error message when user is not owner."""
        self.grant(self.participant)

        self.client.force_login(self.participant)

        response = self.grant(self.participant)
        response_dict = json.loads(response.content)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_dict["message"], "You must be the owner of this activity to perform this action.")

        response = self.remove(self.participant)
        response_dict = json.loads(response.content)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_dict["message"], "You must be the owner of this activity to perform this action.")

    def test_not_logged_in(self):
        """Return an error message when user is logged in."""
        self.client.logout()

        response = self.grant(self.participant)
        response_dict = json.loads(response.content)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_dict["message"], "Authentication credentials were not provided.")

        response = self.remove(self.participant)
        response_dict = json.loads(response.content)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_dict["message"], "Authentication credentials were not provided.")
