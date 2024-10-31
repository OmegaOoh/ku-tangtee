"""Module to test on profile creation handler."""
import json
import django.test
from .shortcuts import create_profile, create_test_user


class CreateProfileTest(django.test.TestCase):
    """Test Cases for Profile Creation."""

    def test_valid_profile_creation(self):
        """Show message when create profile."""
        user = create_test_user("Alexa")
        self.client.force_login(user)
        response, profile = create_profile(user=user)
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(response.content,
                             {'message': 'You have successfully created your KU Tangtee profile.', 'id': profile.id})

    def test_duplicated_profile_creation(self):
        """Show error message when create profile."""
        user = create_test_user("Bruce")
        self.client.force_login(user)
        _, _ = create_profile(user=user)
        response, profile = create_profile(user=user)
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'message': "You've already created your profile.", 'id': profile.id})
