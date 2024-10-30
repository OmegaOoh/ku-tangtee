"""Test for profile model of activities app."""
from datetime import datetime, timedelta

import django.test
from .shortcuts import create_profile, create_test_user
from ..models import Profile

class TestActivityModel(django.test.TestCase):
    """TestCase Class for Profile model."""

    def test_str(self):
        """__str__ returns Profile name."""
        data = {
            "faculty": "Engineering",
            "major": "SKE"
        }
        user = create_test_user('Alexa')
        _, profile = create_profile(user=user, data=data)
        self.assertEqual(str(profile), "Alexa's profile")

    def test_has_profile(self):
        """has_profile() return True if and only if the user has created the profile."""
        user = create_test_user('Alexa')
        _, profile = create_profile(user=user)
        self.assertTrue(Profile.has_profile(user))

    def test_does_not_have_profile(self):
        """has_profile() return False if and only if the user has not created the profile."""
        user = create_test_user('Bruce')
        self.assertFalse(Profile.has_profile(user))
