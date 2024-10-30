"""Test for activity model of activities app."""
import django.test
from .shortcuts import create_activity, create_test_user, client_join_activity
from ..models import Attend
from django import urls
import re
import json


class CheckinTest(django.test.TestCase):
    
    def setUp(self):
        """Set up the common URL."""
        self.url = lambda id: urls.reverse("activities:checkin", args=[id])
        
        self.host = create_test_user('Host')
        _, self.activity = create_activity(host=self.host, client=self.client)
        
        self.attendee = create_test_user('Attendee')
        client_join_activity(client=self.client, user=self.attendee, activity=self.activity)
        self.client.logout()
        
    def test_only_host_can_open(self):
        self.client.force_login(self.attendee)
        res = self.client.put(self.url(self.activity.id) + '?status=open')
        self.assertJSONEqual(res.content, {'message': 'User must be the host to perform this action.'})
        
    def test_host_can_open_check_in(self):
        self.client.force_login(self.host)
        res = self.client.put(self.url(self.activity.id) + '?status=open')
        res_dict = json.loads(res.content)
        
        self.assertEqual(res_dict['message'], 'Activity check-in are open')
        self.assertRegex(res_dict['check_in_code'], r'^[A-Z]{6}$')
        
        self.activity.refresh_from_db()
        
        self.assertTrue(self.activity.check_in_allowed)
        self.assertEqual(self.activity.check_in_code, res_dict['check_in_code'])
        
    def test_host_can_close_check_in(self):
        self.client.force_login(self.host)
        res = self.client.put(self.url(self.activity.id) + '?status=close')
        self.assertJSONEqual(res.content, {'message': 'Activity check-in are close'})
        
        self.activity.refresh_from_db()
        
        self.assertFalse(self.activity.check_in_allowed)
        self.assertIsNone(self.activity.check_in_code)
    
    def test_invalid_status(self):
        self.client.force_login(self.host)
        res = self.client.put(self.url(self.activity.id) + '?status=yes')
        self.assertJSONEqual(res.content, {'message': 'No status provided.'})
        self.activity.refresh_from_db()
        self.assertFalse(self.activity.check_in_allowed)
        
    def test_no_status(self):
        self.client.force_login(self.host)
        res = self.client.put(self.url(self.activity.id))
        self.assertJSONEqual(res.content, {'message': 'No status provided.'})
        self.activity.refresh_from_db()
        self.assertFalse(self.activity.check_in_allowed)
        
    def test_open_and_close(self):
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

    
    
    
