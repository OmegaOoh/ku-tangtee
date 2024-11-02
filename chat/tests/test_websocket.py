"""Test module for chat websocket."""
import django.test
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from activities.models import Activity, Attend
from chat.models import Attachment, Message
from mysite.asgi import application
from django.utils import timezone
from asgiref.sync import async_to_sync, sync_to_async
from activities.tests.constants import CAMERA_EXPECTED_CHAT, CAMERA_IMAGE, BASE64_IMAGE

User = get_user_model()


class ChatWebSocketTest(django.test.TransactionTestCase):
    """Test for chat message websocket."""

    def setUp(self):
        """Create test users and activity."""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.activity = Activity.objects.create(
            name="Test Activity",
            detail="This is a test activity",
            date=timezone.now(),
        )
        Attend.objects.create(user=self.user, activity=self.activity)

    def test_websocket_connection(self):
        """Test if WebSocket connection can be established and messages exchanged."""
        # Simulate user login (for WebSocket authentication)
        self.client.login(username='testuser', password='password123')
        # Define async test for WebSocket connection and messaging

        async def async_test():
            # Initialize WebSocket communicator with ASGI application
            communicator = WebsocketCommunicator(application, f"/ws/chat/{self.activity.id}")
            communicator.scope['user'] = self.user
            # Connect to the WebSocket
            connected, subprotocol = await communicator.connect()
            self.assertTrue(connected, "WebSocket connection failed.")

            # Send a test message
            await communicator.send_json_to({
                "message": "Test Message",
            })
            # Receive message from WebSocket
            response = await communicator.receive_json_from()
            self.assertEqual(response["message"], "Test Message")
            # Close WebSocket connection
            await communicator.disconnect()
        # Run the async test using async_to_sync
        async_to_sync(async_test)()

    def test_send_message_with_image(self):
        """Test if image can be sent along with the message."""
        # Simulate user login (for WebSocket authentication)
        self.client.login(username='testuser', password='password123')
        # Define async test for WebSocket connection and messaging

        async def async_test():
            # Initialize WebSocket communicator with ASGI application
            communicator = WebsocketCommunicator(application, f"/ws/chat/{self.activity.id}")
            communicator.scope['user'] = self.user
            # Connect to the WebSocket
            connected, subprotocol = await communicator.connect()
            self.assertTrue(connected, "WebSocket connection failed.")

            # Send a test message along with image
            await communicator.send_json_to({
                "message": "Test Message",
                "images": [CAMERA_IMAGE]
            })
            # Receive message from WebSocket
            response = await communicator.receive_json_from()
            self.assertEqual(response["message"], "Test Message")
            attachments = response['images'][0]
            expected_url = CAMERA_EXPECTED_CHAT
            self.assertEqual(expected_url, attachments)
            attachment = await sync_to_async(lambda: Attachment.objects.filter(message__message="Test Message").first())()
            if attachment and attachment.image:
                await sync_to_async(attachment.image.delete)()
                await sync_to_async(attachment.delete)()
            # Close WebSocket connection
            await communicator.disconnect()
        # Run the async test using async_to_sync
        async_to_sync(async_test)()

    def test_send_message_with_image_base64(self):
        """Test if image but image is base64 format."""
        # Simulate user login (for WebSocket authentication)
        self.client.login(username='testuser', password='password123')
        # Define async test for WebSocket connection and messaging

        async def async_test():
            # Initialize WebSocket communicator with ASGI application
            communicator = WebsocketCommunicator(application, f"/ws/chat/{self.activity.id}")
            communicator.scope['user'] = self.user
            # Connect to the WebSocket
            connected, subprotocol = await communicator.connect()
            self.assertTrue(connected, "WebSocket connection failed.")

            # Send a test message along with image
            await communicator.send_json_to({
                "message": "Test Message along with base64",
                "images": [BASE64_IMAGE]
            })
            # Receive message from WebSocket
            response = await communicator.receive_json_from()
            self.assertEqual(response["message"], "Test Message along with base64")
            attachments = response['images'][0]
            message = await sync_to_async(lambda: Message.objects.filter(message="Test Message along with base64").first())()
            expected_url = f"/media/chat/{message.id}_attachment_1.jpg"
            self.assertEqual(expected_url, attachments)
            attachment = await sync_to_async(lambda: Attachment.objects.filter(message__message="Test Message along with base64").first())()
            if attachment and attachment.image:
                await sync_to_async(attachment.image.delete)()
                await sync_to_async(attachment.delete)()
            # Close WebSocket connection
            await communicator.disconnect()
        # Run the async test using async_to_sync
        async_to_sync(async_test)()
