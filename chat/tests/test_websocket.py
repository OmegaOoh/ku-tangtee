"""Test module for chat websocket."""
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase
from activities.models import Activity, Attend
from mysite.asgi import application
from django.utils import timezone
from asgiref.sync import async_to_sync
from MySQLdb import OperationalError

User = get_user_model()


class ChatWebSocketTest(TransactionTestCase):
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
            try:
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
            except OperationalError as e:
                print(f"MySQL error occurred: {e}")
                raise
        # Run the async test using async_to_sync
        async_to_sync(async_test)()
