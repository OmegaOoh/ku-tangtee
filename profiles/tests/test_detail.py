"""Module to test on profile page."""
import json
import django.test
from django import urls
from .shortcuts import create_profile, create_test_user
from profiles.serializer.model_serializers import ProfilesSerializer


class DetailTest(django.test.TestCase):
    """Test Cases for Profile View."""

    def setUp(self):
        self.has_profile = [{'has_profile': True}]
        self.not_have_profile = [{'has_profile': False}]

    def test_detail_does_not_have_profile(self):
        """Past activities should not be accessible."""
        response = self.client.get(urls.reverse("profiles:detail"))
        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(response.content, self.not_have_profile)

    def test_detail_has_profile(self):
        """Future/Upcoming activity should be accessible."""
        user = create_test_user("Alexa")
        self.client.force_login(user)

        _, profile = create_profile(user=user)

        response = self.client.get(urls.reverse("profiles:detail"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [ProfilesSerializer(profile).data] + self.has_profile)
