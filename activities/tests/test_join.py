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
        self.url = lambda id: urls.reverse("activities:join", args=[id])

    def test_logout_join(self):
        """Join should respond with error if user are not authenticated."""
        _, new_act = create_activity(host=self.host)
        self.client.logout()

        response = self.client.post(self.url(new_act.id))
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'message': 'Authentication credentials were not provided.'})

    def test_join_without_profile(self):
        """User without profile will unable to join an activity."""
        _, new_act = create_activity(host=self.host)
        self.client.logout()

        attendee = create_test_user("attendee", with_profile=False)
        self.client.force_login(attendee)

        response = self.client.post(self.url(new_act.id))
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'message': 'User must have profile page before joining an activity'})

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

        self.assertJSONEqual(response.content, {'message': f'You have successfully joined the activity {new_act.name}'})

    def test_join_not_exist_actitvity(self):
        """User should unable to join activity that not exist."""
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
        self.assertEqual(response.status_code, 403)
        new_act.refresh_from_db()
        self.assertEqual(new_act.people, 1)
        self.assertNotIn(attender, new_act.participants())

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
        self.assertEqual(response.status_code, 403)
        new_act.refresh_from_db()
        self.assertEqual(new_act.people, 2)
        self.assertIn(attender, new_act.participants())

        self.assertJSONEqual(response.content, {'message': f"You've already joined the activity {new_act.name}."})

    def test_logout_leave(self):
        """Join should respond with error if user are not authenticated."""
        _, new_act = create_activity(host=self.host)

        self.client.logout()
        response = self.client.delete(self.url(new_act.id))
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'message': 'Authentication credentials were not provided.'})

    def test_leave_activity(self):
        """User should able to leave activity that they've join."""
        _, new_act = create_activity(host=self.host)

        attender = create_test_user("Attend")
        self.client.force_login(attender)

        _ = self.client.post(self.url(new_act.id))
        new_act.refresh_from_db()
        self.assertEqual(new_act.people, 2)

        response = self.client.delete(self.url(new_act.id))
        new_act.refresh_from_db()
        self.assertEqual(new_act.people, 1)

        self.assertNotIn(attender, new_act.participants())

        self.assertJSONEqual(response.content, {'message': f"You've successfully leave {new_act.name}"})
        # self.assertJSONEqual(response.content, {'message': f"You've already joined the activity {new_act.name}."})

    def test_leave_not_exist_activity(self):
        """User should unable to leave activity that doesn't exist."""
        attender = create_test_user("Attend")
        self.client.force_login(attender)

        response = self.client.delete(self.url(9999))

        self.assertJSONEqual(response.content, {'message': "You've never join this activity"})

    def test_leave_activity_that_they_havent_join(self):
        """User should not leave activity that the haven't join."""
        _, new_act = create_activity(host=self.host)

        attendee = create_test_user("Attend")
        self.client.force_login(attendee)

        response = self.client.delete(self.url(new_act.id))

        self.assertJSONEqual(response.content, {'message': "You've never join this activity"})

    def test_join_limit_exceed(self):
        """User shouldn't able to join activity if their limit is met."""
        _, new_act1 = create_activity(host=self.host)
        _, new_act2 = create_activity(host=self.host)
        _, new_act3 = create_activity(host=self.host)
        _, new_act4 = create_activity(host=self.host)

        attendee = create_test_user("Attend")
        self.client.force_login(attendee)

        for act in [new_act1, new_act2, new_act3]:
            self.client.post(self.url(act.id))

        res = self.client.post(self.url(new_act4.id))

        self.assertEqual(res.status_code, 403)
        self.assertJSONEqual(res.content, {"message": "The number of activities you have joined has reached the limit"})
