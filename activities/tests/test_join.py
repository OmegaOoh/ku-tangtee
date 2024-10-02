import django.test
from django import urls
from .shortcuts import create_activity

class JoinTest(django.test.TestCase):
    """Test Cases for join function"""
    def test_join_redirection(self):
        """Join redirect user to activity detail page."""
        activity = create_activity("Joinable", 1)
        response = self.client.post(urls.reverse("activities:join", args=[activity.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, urls.reverse("activities:detail", args=[activity.id]))
    
    def test_join_joinable(self):
        """Join will increase number of people in activity."""
        activity = create_activity("Joinable", 1, 8, 10)
        self.client.post(urls.reverse("activities:join", args=[activity.id]))
        self.assertEqual(activity.people, 9)

    def test_join_joinable(self):
        """Join will not increase number of people in activity as activities is full."""
        activity = create_activity("Joinable", 1, 10, 10)
        self.client.post(urls.reverse("activities:join", args=[activity.id]))
        self.assertEqual(activity.people, 10)
