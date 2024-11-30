"""Test for profile model of activities app."""
import django.test

from ..models import Profile
from .shortcuts import create_profile, create_test_user


class TestActivityModel(django.test.TestCase):
    """TestCase Class for Profile model."""

    def test_str(self):
        """__str__ returns Profile name."""
        data = {
            "faculty": "Engineering",
            "ku_generation": "83"
        }
        user = create_test_user('Alexa')
        _, profile = create_profile(user=user, data=data)
        self.assertEqual(str(profile), "Alexa's profile")

    def test_attributes(self):
        """Check if attributes are set correctly."""
        data = {
            "nick_name": "Alex",
            "pronoun": "He/Him",
            "ku_generation": 83,
            "faculty": "Engineering",
            "major": "Software and Knowledge Engineering",
            "about_me": "A passionate coder and fencing enthusiast."
        }
        user = create_test_user('Alexa')
        response, profile = create_profile(user=user, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.faculty, "Engineering")
        self.assertEqual(profile.major, "Software and Knowledge Engineering")
        self.assertEqual(profile.nick_name, "Alex")
        self.assertEqual(profile.pronoun, "He/Him")
        self.assertEqual(profile.ku_generation, 83)
        self.assertEqual(profile.about_me, "A passionate coder and fencing enthusiast.")

    def test_has_profile(self):
        """has_profile() return True if and only if the user has created the profile."""
        user = create_test_user('Alexa')
        _, _ = create_profile(user=user)
        self.assertTrue(Profile.has_profile(user))

    def test_does_not_have_profile(self):
        """has_profile() return False if and only if the user has not created the profile."""
        user = create_test_user('Bruce')
        _, _ = create_profile()
        self.assertFalse(Profile.has_profile(user))
