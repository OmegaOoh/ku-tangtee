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
        response, profile = create_profile(user=user, data=data, days_delta=0)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.faculty, "Engineering")
        self.assertEqual(profile.major, "Software and Knowledge Engineering")
        self.assertEqual(profile.nick_name, "Alex")
        self.assertEqual(profile.date_of_birth, datetime.today().date())
        self.assertEqual(profile.pronoun, "He/Him")
        self.assertEqual(profile.ku_generation, 83)
        self.assertEqual(profile.about_me, "A passionate coder and fencing enthusiast.")

    def test_has_profile(self):
        """has_profile() return True if and only if the user has created the profile."""
        user = create_test_user('Alexa')
        _, profile = create_profile(user=user)
        self.assertTrue(Profile.has_profile(user))

    def test_does_not_have_profile(self):
        """has_profile() return False if and only if the user has not created the profile."""
        user = create_test_user('Bruce')
        self.assertFalse(Profile.has_profile(user))

    def test_age(self):
        """age return user's age."""
        data = {
            "faculty": "Engineering",
            "major": "SKE",
        }
        user = create_test_user('Clark')
        _, profile = create_profile(user=user, data=data, days_delta=25*365 + 20)
        self.assertEqual(profile.age, 25)
