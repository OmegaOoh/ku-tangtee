"""Module to test on index page of activities app."""
import django.test
from django import urls

from .shortcuts import create_activity, activity_to_json, create_test_user, convert_day_num, date_from_now


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
        create_activity(host=self.host_user, days_delta=-1)
        response = self.client.get(urls.reverse("activities:index"))
        self.assertJSONEqual(response.content, [])

    def test_future_and_past_activity(self):
        """Only activities take place in the future is showed on index page."""
        _, activity = create_activity(host=self.host_user)
        create_activity(host=self.host_user, days_delta=-1)
        response = self.client.get(urls.reverse("activities:index"))
        expected = [
            activity_to_json(activity)
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
        """Only activities whose name or detail regex match with keyword is shown on index page."""
        _, activity1 = create_activity(
            host=self.host_user,
            data={"name": "tes1", "detail": "12"}
        )

        _, activity2 = create_activity(
            host=self.host_user,
            data={"name": "test2", "detail": "en"}
        )

        _, activity3 = create_activity(
            host=self.host_user,
            data={"name": "12", "detail": "garde"}
        )

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

    def test_search_by_date_range(self):
        """Only activities within the date range is shown on index page."""
        _, activity1 = create_activity(
            host=self.host_user,
            data={"name": "+1day", "detail": "+1day"},
            days_delta=1
        )
        act1_day = date_from_now(1)

        _, activity2 = create_activity(
            host=self.host_user,
            data={"name": "+2day", "detail": "+2day"},
            days_delta=2
        )
        act2_day = date_from_now(2)

        _, activity3 = create_activity(
            host=self.host_user,
            data={"name": "+3day", "detail": "+3day"},
            days_delta=3
        )
        act3_day = date_from_now(3)

        _, activity7 = create_activity(
            host=self.host_user,
            data={"name": "+7day", "detail": "+7day"},
            days_delta=7
        )
        act7_day = date_from_now(7)

        today = date_from_now(0)
        next_year = date_from_now(365)

        json_act1 = activity_to_json(activity1)
        json_act2 = activity_to_json(activity2)
        json_act3 = activity_to_json(activity3)
        json_act7 = activity_to_json(activity7)

        response = self.client.get(urls.reverse("activities:index") + f"?start_date={today}")
        self.assertJSONEqual(response.content, [json_act1, json_act2, json_act3, json_act7])

        response = self.client.get(urls.reverse("activities:index") + f"?start_date={act3_day}")
        self.assertJSONEqual(response.content, [json_act3, json_act7])

        response = self.client.get(urls.reverse("activities:index") + f"?start_date={next_year}")
        self.assertJSONEqual(response.content, [])

        response = self.client.get(urls.reverse("activities:index") + f"?end_date={next_year}")
        self.assertJSONEqual(response.content, [json_act1, json_act2, json_act3, json_act7])

        response = self.client.get(urls.reverse("activities:index") + f"?end_date={act3_day}")
        self.assertJSONEqual(response.content, [json_act1, json_act2, json_act3])

        response = self.client.get(urls.reverse("activities:index") + f"?end_date={today}")
        self.assertJSONEqual(response.content, [])

        response = self.client.get(urls.reverse("activities:index") + f"?start_date={act2_day}&end_date={act3_day}")
        self.assertJSONEqual(response.content, [json_act2, json_act3])

        response = self.client.get(urls.reverse("activities:index") + f"?start_date={act2_day}&end_date={act2_day}")
        self.assertJSONEqual(response.content, [json_act2])

        response = self.client.get(urls.reverse("activities:index") + f"?start_date={act7_day}&end_date={act1_day}")
        self.assertJSONEqual(response.content, [])

        response = self.client.get(urls.reverse("activities:index") + f"?start_date={act3_day}&end_date=invalid")
        self.assertJSONEqual(response.content, [json_act3, json_act7])

        response = self.client.get(urls.reverse("activities:index") + f"?start_date=invalid&end_date={act3_day}")
        self.assertJSONEqual(response.content, [json_act1, json_act2, json_act3])

        response = self.client.get(urls.reverse("activities:index") + "?start_date=9999-99-99&end_date=invalid")
        self.assertJSONEqual(response.content, [json_act1, json_act2, json_act3, json_act7])

        response = self.client.get(urls.reverse("activities:index") + "?start_date=invalid")
        self.assertJSONEqual(response.content, [json_act1, json_act2, json_act3, json_act7])

        response = self.client.get(urls.reverse("activities:index") + "?start_date=9999-99-99")
        self.assertJSONEqual(response.content, [json_act1, json_act2, json_act3, json_act7])

        response = self.client.get(urls.reverse("activities:index") + "?start_date=")
        self.assertJSONEqual(response.content, [json_act1, json_act2, json_act3, json_act7])

        response = self.client.get(urls.reverse("activities:index") + "?end_date=invalid")
        self.assertJSONEqual(response.content, [json_act1, json_act2, json_act3, json_act7])

        response = self.client.get(urls.reverse("activities:index") + "?end_date=9999-99-99")
        self.assertJSONEqual(response.content, [json_act1, json_act2, json_act3, json_act7])

        response = self.client.get(urls.reverse("activities:index") + "?end_date=")
        self.assertJSONEqual(response.content, [json_act1, json_act2, json_act3, json_act7])
