"""Module on test activity owner access granting and removing."""
import json
import django.test
from django import urls
from activities import models
from .shortcuts import activity_to_json, client_join_activity, create_activity, create_test_user, put_request_json_data
from django.utils import timezone

from ..models import Attend


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

        # Set the URL to the host access edit page
        self.grant_url = lambda user: urls.reverse("activities:host", args=["grant", self.activity.id, user.id])
        self.remove_url = lambda user: urls.reverse("activities:host", args=["remove", self.activity.id, user.id])

    def test_grant_and_remove_host(self):
        """Return a success message and user gain and lose host access for activity accordingly."""
        self.assertEqual(self.activity.host(), [self.owner])

        # Send PUT request for grant
        response = put_request_json_data(self.grant_url(self.participant), self.client, {})
        response_dict = json.loads(response.content)
        self.assertEqual(self.activity.host(), [self.owner, self.participant])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict["message"], f"You have successfully granted host access to user {self.participant.username} for activity {self.activity.name}.")

        # Send PUT request for remove
        response = put_request_json_data(self.remove_url(self.participant), self.client, {})
        response_dict = json.loads(response.content)
        self.assertEqual(self.activity.host(), [self.owner])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict["message"], f"You have successfully removed host access to user {self.participant.username} for activity {self.activity.name}.")

    def test_remove_host(self):
        """Return a success message and user host access for activity is removed."""
        response = put_request_json_data(self.remove_url(self.participant), self.client, {})
        response_dict = json.loads(response.content)
        self.assertEqual(self.activity.host(), [self.owner])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict["message"], f"You have successfully removed host access to user {self.participant.username} for activity {self.activity.name}.")

    def test_grant_host_for_non_participants(self):
        """Return an error message when grant host for non-participants."""
        # Send PUT request with new activity data
        response = put_request_json_data(self.grant_url(self.user), self.client, {})
        response_dict = json.loads(response.content)
        self.assertEqual(self.activity.host(), [self.owner])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_dict["message"], f"Cannot find user {self.user.username} in this activity.")

    def test_remove_host_for_non_participants(self):
        """Return an error message when remove host for non-participants."""
        # Send PUT request with new activity data
        response = put_request_json_data(self.remove_url(self.user), self.client, {})
        response_dict = json.loads(response.content)
        self.assertEqual(self.activity.host(), [self.owner])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_dict["message"], f"Cannot find user {self.user.username} in this activity.")

    def test_grant_host_owner(self):
        """Return an error message when grant host for owner."""
        # Send PUT request with new activity data
        response = put_request_json_data(self.grant_url(self.owner), self.client, {})
        response_dict = json.loads(response.content)
        self.assertEqual(self.activity.host(), [self.owner])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_dict["message"], 'Cannot modify access of your own activity.')

    def test_remove_host_owner(self):
        """Return an error message when remove host for owner."""
        # Send PUT request with new activity data
        response = put_request_json_data(self.remove_url(self.owner), self.client, {})
        response_dict = json.loads(response.content)
        self.assertEqual(self.activity.host(), [self.owner])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_dict["message"], "Cannot modify access of your own activity.")

    def test_not_owner(self):
        """Return an error message when user is not owner."""
        self.client.logout()
        self.client.force_login(self.participant)
        response = put_request_json_data(self.grant_url(self.participant), self.client, {})
        response_dict = json.loads(response.content)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_dict["message"], "You must be the owner of this activity to perform this action.")

    def test_not_logged_in(self):
        """Return an error message when user is logged in."""
        self.client.logout()
        response = put_request_json_data(self.remove_url(self.participant), self.client, {})
        response_dict = json.loads(response.content)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_dict["message"], "Authentication credentials were not provided.")
