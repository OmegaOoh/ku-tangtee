"""Test module for check-in behaviour."""
import django.test
from .shortcuts import create_activity, create_test_user, client_join_activity
from ..models import Attend
from django import urls
import re
import json


class CheckinTest(django.test.TestCase):
    """Test check-in behaviors."""

    def setUp(self):
        """Set up the common URL and common value."""
        self.url = lambda id: urls.reverse("activities:checkin", args=[id])

        self.host = create_test_user('Host')
        _, self.activity = create_activity(host=self.host, client=self.client)

        self.attendee = create_test_user('Attendee')
        client_join_activity(client=self.client, user=self.attendee, activity=self.activity)
        self.client.logout()

    def test_only_host_can_open(self):
        """Only host can open a check-in."""
        self.client.force_login(self.attendee)
        res = self.client.put(self.url(self.activity.id) + '?status=open')
        self.assertJSONEqual(res.content, {'message': 'User must be the host to perform this action.'})

    def test_host_can_open_check_in(self):
        """Host should able to open for participant to check-in."""
        self.client.force_login(self.host)
        res = self.client.put(self.url(self.activity.id) + '?status=open')
        res_dict = json.loads(res.content)

        self.assertEqual(res_dict['message'], 'Activity check-in are open')
        self.assertRegex(res_dict['check_in_code'], r'^[A-Z]{6}$')

        self.activity.refresh_from_db()

        self.assertTrue(self.activity.check_in_allowed)
        self.assertEqual(self.activity.check_in_code, res_dict['check_in_code'])

    def test_host_can_close_check_in(self):
        """Host shoud able to close for participant to check-in."""
        self.client.force_login(self.host)
        res = self.client.put(self.url(self.activity.id) + '?status=close')
        self.assertJSONEqual(res.content, {'message': 'Activity check-in are close'})

        self.activity.refresh_from_db()

        self.assertFalse(self.activity.check_in_allowed)
        self.assertIsNone(self.activity.check_in_code)

    def test_invalid_status(self):
        """Nothing should change is query param is invalid."""
        self.client.force_login(self.host)
        res = self.client.put(self.url(self.activity.id) + '?status=yes')
        self.assertJSONEqual(res.content, {'message': 'No status provided.'})
        self.activity.refresh_from_db()
        self.assertFalse(self.activity.check_in_allowed)

    def test_no_status(self):
        """Nothing should change if query param status are not provided."""
        self.client.force_login(self.host)
        res = self.client.put(self.url(self.activity.id))
        self.assertJSONEqual(res.content, {'message': 'No status provided.'})
        self.activity.refresh_from_db()
        self.assertFalse(self.activity.check_in_allowed)

    def test_host_open_and_close(self):
        """Host should able to open and close for participant to check-in."""
        self.client.force_login(self.host)

        self.client.force_login(self.host)
        res = self.client.put(self.url(self.activity.id) + '?status=open')
        res_dict = json.loads(res.content)

        self.assertEqual(res_dict['message'], 'Activity check-in are open')
        self.assertRegex(res_dict['check_in_code'], r'^[A-Z]{6}$')
        self.activity.refresh_from_db()
        self.assertTrue(self.activity.check_in_allowed)
        self.assertEqual(self.activity.check_in_code, res_dict['check_in_code'])

        res = self.client.put(self.url(self.activity.id) + '?status=close')
        self.assertJSONEqual(res.content, {'message': 'Activity check-in are close'})
        self.activity.refresh_from_db()
        self.assertFalse(self.activity.check_in_allowed)

    def test_logout_check_in(self):
        """Unauthenticated user should able to check-in."""
        res = self.client.post(self.url(self.activity.id))
        self.assertJSONEqual(res.content, {'message': 'Authentication credentials were not provided.'})

    def test_not_a_member_check_in(self):
        """User that are not the participant of activity should not able to check-in."""
        self.open()
        new_user = create_test_user('Not a member')
        self.client.force_login(new_user)
        res = self.client.post(
            self.url(self.activity.id),
            data={
                'check_in_code': self.activity.check_in_code
            }
        )
        self.assertJSONEqual(res.content, {'message': "You're not member of this activity"})

    def test_check_in_close(self):
        """User should unavailable to check-in when host is close the check-in."""
        self.open()
        self.close()
        self.client.force_login(self.attendee)
        res = self.client.post(
            self.url(self.activity.id),
            data={
                'check_in_code': self.activity.check_in_code
            }
        )
        self.assertJSONEqual(res.content, {'message': 'Check-in are not allow at the moment'})
        self.assertFalse(self.attendee.attend_set.get(activity=self.activity).checked_in)

    def test_wrong_check_in_code(self):
        """User should not check-in if check-in code are not match."""
        self.open()

        self.client.force_login(self.attendee)
        res = self.client.post(
            self.url(self.activity.id),
            data={
                'check_in_code': 'wrongs'
            }
        )
        self.assertJSONEqual(res.content, {'message': 'Check-in code invalid'})
        self.assertFalse(self.attendee.attend_set.get(activity=self.activity).checked_in)

    def test_complete_check_in(self):
        """Test success check-in."""
        self.open()

        self.client.force_login(self.attendee)
        res = self.client.post(
            self.url(self.activity.id),
            data={
                'check_in_code': self.activity.check_in_code
            }
        )
        self.assertJSONEqual(res.content, {'message': f"You've successfully check-in to {self.activity.name}"})
        self.assertTrue(self.attendee.attend_set.get(activity=self.activity).checked_in)

    def open(self):
        """Open for check-in."""
        self.client.force_login(self.host)
        self.client.put(self.url(self.activity.id) + '?status=open')
        self.client.logout()
        self.activity.refresh_from_db()

    def close(self):
        """Close check in."""
        self.client.force_login(self.host)
        self.client.put(self.url(self.activity.id) + '?status=close')
        self.client.logout()
        self.activity.refresh_from_db()