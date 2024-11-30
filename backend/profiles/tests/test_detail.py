"""Module to test on profile detail page."""
import django.test
from django import urls
from profiles.serializer.model_serializers import ProfilesSerializer

from .shortcuts import create_profile, create_test_user


class DetailTest(django.test.TestCase):
    """Test Cases for Profile Detail View."""

    def test_detail_other_profile(self):
        """Show other profile creation."""
        user1 = create_test_user("Bruce")
        user2 = create_test_user("Clark")
        _, profile = create_profile(user=user1)

        self.client.force_login(user2)

        response = self.client.get(urls.reverse("profiles:detail", args=[profile.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, ProfilesSerializer(profile).data)

    def test_detail_own_profile(self):
        """Show your own profile information."""
        user = create_test_user("Alexa")
        self.client.force_login(user)
        _, profile = create_profile(user=user)

        response = self.client.get(urls.reverse("profiles:detail", args=[profile.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, ProfilesSerializer(profile).data)
