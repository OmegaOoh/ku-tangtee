"""Test module for chat view."""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from activities.models import Activity
from django.contrib.auth.models import User
from chat.models import Message

class ChatMessageListTest(APITestCase):
    """Test case for the ChatMessageList view."""

    def setUp(self):
        """Create user, login user, create activity and create message."""
        self.activity = Activity.objects.create(name="Test Activity")
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.message1 = Message.objects.create(
            activity=self.activity,
            sender=self.user,
            message="Hello, this is a test message."
        )
        self.message2 = Message.objects.create(
            activity=self.activity,
            sender=self.user,
            message="This is another test message."
        )

    def test_get_chat_messages(self):
        """Test the retrieval of chat messages for an activity."""
        url = reverse('chat_message_list', args=[self.activity.id])  # Adjust the name as needed
        response = self.client.get(url)

        # Check that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the response data matches the messages created
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['message'], self.message1.message)
        self.assertEqual(response.data[1]['message'], self.message2.message)

    def test_get_chat_messages_empty(self):
        """Test retrieval when there are no messages for the activity."""
        url = reverse('chat_message_list', args=[self.activity.id])
        # Delete messages to test empty response
        Message.objects.all().delete()
        response = self.client.get(url)

        # Check that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the response data is empty
        self.assertEqual(response.data, [])
