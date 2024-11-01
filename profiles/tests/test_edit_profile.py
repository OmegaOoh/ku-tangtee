"""Module on test profile editing."""
import json
import django.test
from django import urls
from profiles import models
from .shortcuts import create_test_user, create_profile, put_request_json_data


class EditActivityTest(django.test.TestCase):
    """Test case for editing profile."""

    def setUp(self):
        """Set up the common URL and create a profile."""
        data = {
            "nick_name": "Alex",
            "pronoun": "He/Him",
            "ku_generation": 83,
            "faculty": "Engineering",
            "major": "Software and Knowledge Engineering",
            "about_me": "A passionate coder and fencing enthusiast."
        }
        self.user = create_test_user("user")
        self.client.force_login(self.user)
        _, self.profile = create_profile(user=self.user, data=data)

        # Set the URL to the profile page
        self.url = urls.reverse("profiles:detail", args=[self.profile.id])

        self.edited_data = {
            "nick_name": "Bruce",
            "pronoun": "She/Her",
            "ku_generation": 84,
            "faculty": "Science",
            "major": "Computer Science",
            "about_me": "A passionate coder and swimming enthusiast.",
        }

    def test_valid_profile_editing(self):
        """Edit should return a success message with the updated profile information."""
        # Send PUT request with new profile data
        response = put_request_json_data(self.url, self.client, self.edited_data)
        response_dict = json.loads(response.content)
        updated_profile = models.Profile.objects.get(pk=self.profile.id)
        # Compare the serialized profile with the expected data
        self.assertEqual(updated_profile.nick_name, self.edited_data['nick_name'])
        self.assertEqual(updated_profile.pronoun, self.edited_data['pronoun'])
        self.assertEqual(updated_profile.ku_generation, self.edited_data['ku_generation'])
        self.assertEqual(updated_profile.faculty, self.edited_data['faculty'])
        self.assertEqual(updated_profile.major, self.edited_data['major'])
        self.assertEqual(updated_profile.about_me, self.edited_data['about_me'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict["message"], "You have successfully edited your KU Tangtee profile.")

    def test_other_profile_editing(self):
        """Edit should return an error message when try to edit other profile."""
        hacker = create_test_user("hacker")
        self.client.force_login(hacker)

        response = put_request_json_data(self.url, self.client, self.edited_data)
        response_dict = json.loads(response.content)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_dict["message"], "Cannot edit other profile.")

    def test_not_logged_in(self):
        """Show error message when not logged in."""
        self.client.logout()

        response = put_request_json_data(self.url, self.client, self.edited_data)
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'message': 'Authentication credentials were not provided.'})
