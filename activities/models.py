from django.db import models
from django.utils import timezone
import datetime

class Activity(models.Model):
    """Activity model to store data of activity detail."""
    name = models.CharField(max_length=255, unique=True)
    detail = models.CharField(max_length=1024)
    date = models.DateTimeField(default=timezone.now)
    max_people = models.IntegerField(null=True, blank=True)
    people = models.IntegerField(default=0)

    def __str__(self):
        """Return Activity Name as string representative"""
        return self.name
    
    def can_join(self):
        """Return True if max_people doesn't reached and date doesn't past, Otherwise false."""
        return self.date < datetime.now() and self.people <= self.people
    
    def is_incoming(self):
        """Return True if activities took place on incoming weeks, Otherwise false."""
        return self.date +timezone.timedelta(weeks=1) >= datetime.now()
    