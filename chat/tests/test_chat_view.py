"""Test module for chat view."""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from activities.models import Activity
from django.contrib.auth.models import User
from chat.models import Message, Attachment
from chat.tests.shortcuts import image_loader


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
        self.url = reverse('chat_message_list', args=[self.activity.id])

    def test_get_chat_messages(self):
        """Test the retrieval of chat messages for an activity."""
        response = self.client.get(self.url)

        # Check that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the response data matches the messages created
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['message'], self.message1.message)
        self.assertEqual(response.data[1]['message'], self.message2.message)

    def test_get_chat_messages_empty(self):
        """Test retrieval when there are no messages for the activity."""
        # Delete messages to test empty response
        Message.objects.all().delete()
        response = self.client.get(self.url)

        # Check that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the response data is empty
        self.assertEqual(response.data, [])
    
    def test_get_image_from_message(self):
        """Test getting image that comes along with message."""
        message3 = Message.objects.create(
            activity=self.activity,
            sender=self.user,
            message="Message comes up with image."
        )
        img_url = ["https://static.wixstatic.com/media/11062b_6864d981fa86430f84b3926857b21d8c~mv2.jpg/v1/fill/w_640,h_1058,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/11062b_6864d981fa86430f84b3926857b21d8c~mv2.jpg"]
        image_loader(img_url, message3)
        chat_img = Attachment.objects.filter(message=message3).first()
        chat_img_url = chat_img.image.url
        response = self.client.get(self.url)

        # Check that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['message'], self.message1.message)
        self.assertEqual(response.data[1]['message'], self.message2.message)
        self.assertEqual(response.data[2]['message'], message3.message)
        self.assertEqual(response.data[2]['images'][0], chat_img_url)
        chat_img.image.delete(save=False)
        chat_img.delete()
