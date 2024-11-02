"""Module to test on index page of activities app."""
import django.test
from django import urls
from .shortcuts import create_activity, activity_to_json, create_test_user, convert_day_num


class IndexTest(django.test.TestCase):
    """Test Cases for Index view."""

    def setUp(self):
        """Set up the common URL."""
        self.url = urls.reverse("activities:index")
        self.host_user = create_test_user("Host")

    def test_no_activity(self):
        """If no activities available, an appropriate messages is displayed."""
        response = self.client.get(self.url)
        self.assertJSONEqual(response.content, [])

    def test_future_activity(self):
        """Activities take places in future showed on the index page."""
        response, activity = create_activity(host=self.host_user)
        self.assertEqual(activity.people, 1)
        response = self.client.get(self.url)
        expected = [
            activity_to_json(activity)
        ]
        self.assertJSONEqual(response.content, expected)

    def test_past_activity(self):
        """Activities take places in the past showed on the index page."""
        _, activity = create_activity(host=self.host_user, days_delta=-1)
        response = self.client.get(urls.reverse("activities:index"))
        self.assertJSONEqual(response.content, [activity_to_json(activity)])

    def test_future_and_past_activity(self):
        """Only activities take place in the future is showed on index page."""
        _, activity = create_activity(host=self.host_user)
        _, activity2 = create_activity(host=self.host_user, days_delta=-1)
        response = self.client.get(urls.reverse("activities:index"))
        expected = [
            activity_to_json(activity2),
            activity_to_json(activity),
        ]
        self.assertJSONEqual(response.content, expected)

    def test_two_future_activity(self):
        """Both of activity is showed on index page."""
        _, activity1 = create_activity(host=self.host_user)
        _, activity2 = create_activity(host=self.host_user)
        response = self.client.get(urls.reverse("activities:index"))
        expected = [
            activity_to_json(activity1),
            activity_to_json(activity2)
        ]
        self.assertJSONEqual(response.content, expected)

    def test_search_by_keyword(self):
        """Only activities with keyword in its name or detail showed on index page."""
        _, activity1 = create_activity(host=self.host_user, data={"name": "tes1", "detail": "12"})
        _, activity2 = create_activity(host=self.host_user, data={"name": "test2", "detail": "en"})
        _, activity3 = create_activity(host=self.host_user, data={"name": "12", "detail": "garde"})

        json_act1 = activity_to_json(activity1)
        json_act2 = activity_to_json(activity2)
        json_act3 = activity_to_json(activity3)

        response = self.client.get(urls.reverse("activities:index") + "?keyword=test")
        self.assertJSONEqual(response.content, [json_act2])

        response = self.client.get(urls.reverse("activities:index") + "?keyword=tes")
        self.assertJSONEqual(response.content, [json_act1, json_act2])

        response = self.client.get(urls.reverse("activities:index") + "?keyword=2")
        self.assertJSONEqual(response.content, [json_act1, json_act2, json_act3])

        response = self.client.get(urls.reverse("activities:index") + "?keyword=")
        self.assertJSONEqual(response.content, [json_act1, json_act2, json_act3])

        response = self.client.get(urls.reverse("activities:index") + "?keyword=Engarde")
        self.assertJSONEqual(response.content, [])

    def test_search_by_day_of_week(self):
        """GET req to index with day code (1 = Sunday), index should return list of activity on that day."""
        _, activity1 = create_activity(
            host=self.host_user,
            client=self.client,
            data={"name": "day1", "detail": "12"},
            days_delta=1
        )
        act1_day = convert_day_num(activity1.date.weekday())

        _, activity2 = create_activity(
            host=self.host_user,
            client=self.client,
            data={"name": "day2", "detail": "en"},
            days_delta=2
        )
        act2_day = convert_day_num(activity2.date.weekday())

        _, activity3 = create_activity(
            host=self.host_user,
            client=self.client,
            data={"name": "day3", "detail": "garde"},
            days_delta=3
        )
        act3_day = convert_day_num(activity3.date.weekday())

        _, activity4 = create_activity(
            host=self.host_user,
            client=self.client,
            data={"name": "day4", "detail": "garde"},
            days_delta=4
        )
        act4_day = convert_day_num(activity4.date.weekday())

        res = self.client.get(urls.reverse("activities:index") + f"?day={act1_day}")
        self.assertJSONEqual(res.content, [activity_to_json(activity1)])

        res = self.client.get(urls.reverse("activities:index") + f"?day={act3_day},{act2_day}")
        self.assertJSONEqual(res.content, [activity_to_json(activity2), activity_to_json(activity3)])

        res = self.client.get(urls.reverse("activities:index") + f"?day={act1_day},{act2_day},{act3_day},{act4_day}")
        self.assertJSONEqual(
            res.content,
            [activity_to_json(act) for act in [activity1, activity2, activity3, activity4]]
        )

        res = self.client.get(urls.reverse("activities:index") + "?day=invalid")
        self.assertJSONEqual(
            res.content,
            [activity_to_json(act) for act in [activity1, activity2, activity3, activity4]]
        )

        res = self.client.get(urls.reverse("activities:index") + "?day=10,20,8")
        self.assertJSONEqual(
            res.content,
            [activity_to_json(act) for act in [activity1, activity2, activity3, activity4]]
        )
