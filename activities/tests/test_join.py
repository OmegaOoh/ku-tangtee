"""Test for Join function."""
import django.test
from django import urls
from .shortcuts import create_activity, create_test_user
from activities import models
import json


class JoinTest(django.test.TestCase):
    """Test Cases for join function."""

    def setUp(self):
        """Set up the common URL."""
        self.host = create_test_user("Host")
        self.url = lambda id :urls.reverse("activities:join", args=[id])

    def test_logout_join(self):
        """Join should respond with error if user are not authenticated."""
        _, new_act = create_activity(host=self.host)

        self.client.logout()
        response = self.client.post(self.url(new_act.id))
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'message': 'Authentication credentials were not provided.'})

    def test_join(self):
        """Join will increase number of people in activity."""
        _, new_act = create_activity(host=self.host)

        attender = create_test_user("Attend")
        self.client.force_login(attender)

        self.assertEqual(new_act.people, 1)

        response = self.client.post(self.url(new_act.id))
        self.assertEqual(response.status_code, 201)
        new_act.refresh_from_db()
        self.assertEqual(new_act.people, 2)
        self.assertIn(attender, new_act.participants())

        response_dict = response.json()
        self.assertEqual(response_dict['message'], f'You have successfully joined the activity {new_act.name}')
        
    def test_join_not_exist_actitvity(self):
        
        attender = create_test_user("Attend")
        self.client.force_login(attender)
        
        not_exist_pk = 9999
        
        response = self.client.post(self.url(not_exist_pk))
        self.assertJSONEqual(response.content, {'message': f'Invalid pk "{not_exist_pk}" - object does not exist.'})

    def test_join_full(self):
        """Join will not increase number of people in activity as activities is full."""
        data = {
            "name": "Unjoinable",
            "detail": "This act is unjoinable",
            "max_people": 1
        }
        response, new_act = create_activity(host=self.host, data=data)
        self.assertEqual(response.status_code, 200)

        attender = create_test_user("Attend")
        self.client.force_login(attender)

        response = self.client.post(self.url(new_act.id))
        self.assertEqual(response.status_code, 400)
        new_act.refresh_from_db()
        self.assertEqual(new_act.people, 1)
        self.assertNotIn(attender, new_act.participants())

        response_dict = json.loads(response.content)
        self.assertJSONEqual(response.content, {'message': 'The activity Unjoinable is full.'})

    def test_rejoin_joined_activity(self):
        """Cannot join activity that already joined."""
        _, new_act = create_activity(host=self.host)

        attender = create_test_user("Attend")
        self.client.force_login(attender)

        # First time joined, number of people increase.
        response = self.client.post(self.url(new_act.id))
        new_act.refresh_from_db()
        self.assertEqual(new_act.people, 2)
        self.assertIn(attender, new_act.participants())

        # Second time joined, get error and number of people stays the same.
        response = self.client.post(self.url(new_act.id))
        self.assertEqual(response.status_code, 400)
        new_act.refresh_from_db()
        self.assertEqual(new_act.people, 2)
        self.assertIn(attender, new_act.participants())

        response_dict = json.loads(response.content)
        self.assertJSONEqual(response.content, {'message': f"You've already joined the activity {new_act.name}."})
