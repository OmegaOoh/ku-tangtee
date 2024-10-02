from django.shortcuts import render
from django.utils import timezone
from . import models
from django.views import generic

class IndexView(generic.ListView):
    """View class to show all upcoming activities"""
    model = models.Activity
    template_name = "activities/index.html"
    context_object_name = "activities"

    def get_queryset(self):
        """ 
        Return Queryset of activities that is not took place yet.
        
        Queryset is order by date that the activity took place.(ealier to later)
        """
        return models.Activity.objects.filter(date__gte=timezone.now()).order_by("date")
    