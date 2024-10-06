"""Module to test on activity creation"""
import json
import django.test
from datetime import datetime
from django import urls
from django.utils import timezone
from activities import models

class CreateActivityTest(django.test.TestCase):
    """Test case for creating activity"""
    
    def setUp(self):
        self.url = urls.reverse("activities:create")
    
    def test_get_request(self):
        """Create should return error message when got a GET request"""
                
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "Forbidden access"})
        
    def test_valid_activity_creation_without_date_and_max_people(self):
        """Create should return message with successful message and activity name"""
        
        data = {
            "name": "Valid Activity",
            "detail": "This is valid activity",
        }
        
        response = self.client.post(self.url, data=data)
        response_dict = json.loads(response.content)
        
        new_act = models.Activity.objects.get(pk=int(response_dict["id"]))
                
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict["message"], f"Your have successfully create activity {data.get('name')}")
        self.assertEqual(new_act.name, data.get('name'))
        self.assertEqual(new_act.people, 1)
        
    def test_valid_activity_creation_with_date(self):
        """Create should return message with successful message and activity name"""
        
        data = {
            "name": "Valid Activity",
            "detail": "This is valid activity",
            "date": "2024-10-10T10:20"
        }
        
        response = self.client.post(self.url, data=data)
        response_dict = json.loads(response.content)
        
        new_act = models.Activity.objects.get(pk=int(response_dict["id"]))
                
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict["message"], f"Your have successfully create activity {data.get('name')}")
        self.assertEqual(new_act.name, data.get('name'))
        self.assertEqual(new_act.people, 1)
        self.assertEqual(new_act.date, timezone.make_aware(datetime.strptime(data["date"],  "%Y-%m-%dT%H:%M")))

    def test_valid_activity_creation_with_max_people(self):
        """Create should return message with successful message and activity name"""
        
        data = {
            "name": "Valid Activity",
            "detail": "This is valid activity",
            "max_people": 10
        }
        
        response = self.client.post(self.url, data=data)
        response_dict = json.loads(response.content)
        
        new_act = models.Activity.objects.get(pk=int(response_dict["id"]))
                
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict["message"], f"Your have successfully create activity {data.get('name')}")
        self.assertEqual(new_act.name, data.get('name'))
        self.assertEqual(new_act.people, 1)
        self.assertEqual(new_act.max_people, data.get("max_people"))
        
    def test_valid_activity_creation_with_date_and_max_people(self):
        """Create should return json with successful message and activity name"""
        
        data = {
            "name": "Valid Activity",
            "detail": "This is valid activity",
            "date": "2024-10-10T10:20",
            "max_people": 10
        }
        
        response = self.client.post(self.url, data=data)
        response_dict = json.loads(response.content)
        
        new_act = models.Activity.objects.get(pk=response_dict["id"])
                
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_dict["message"], f"Your have successfully create activity {data.get('name')}")
        self.assertEqual(new_act.name, data.get('name'))
        self.assertEqual(new_act.people, 1)
        self.assertEqual(new_act.max_people, data.get("max_people"))
        
    def test_invalid_activity_creation_without_name(self):
        """Create should return error with error message"""
        
        data = {
            "detail": "This isinvalid activity",
            "date": "2024-10-10T10:20",
            "max_people": 10
        }
        
        response = self.client.post(self.url, data=data)                                
        self.assertEqual(response.status_code, 400)
        
        response_dict = json.loads(response.content)
        self.assertIn("Error occur", response_dict["error"])
        
    def test_invalid_activity_creation_with_wrong_date_format(self):
        """Create should return json with error message """
        
        data = {
            "name": "Wrong date format", 
            "detail": "This is invalid activity",
            "date": "2024-10-10T10:20",
            "max_people": 10
        }
        
        response = self.client.post(self.url, data=data)                                
        self.assertEqual(response.status_code, 400)
        
        response_dict = json.loads(response.content)
        self.assertIn("Error occur", response_dict["error"])
        
    def test_invalid_activity_creation_with_too_long_activity_name(self):
        """Create should return json with error message """
        
        data = {
            "name": "This is too long" * 50, 
            "detail": "This is invalid activity",
            "date": "2024-10-10T10:20",
            "max_people": 10
        }
        
        response = self.client.post(self.url, data=data)                                
        self.assertEqual(response.status_code, 400)
        
        response_dict = json.loads(response.content)
        self.assertIn("Error occur", response_dict["error"])
        
    def test_invalid_activity_creation_with_wrong_type_data(self):
        """Create should return json with error message """
        
        data = {
            "name": 10, 
            "detail": "This is invalid activity",
            "date": "2024-10-10T10:20",
            "max_people": 10
        }
        
        response = self.client.post(self.url, data=data)                                
        self.assertEqual(response.status_code, 400)
        
        response_dict = json.loads(response.content)
        self.assertIn("Error occur", response_dict["error"])
        
    
    
    