"""Register models to manipulate in admin site of django."""
from django.contrib import admin
from . import models

admin.site.register(models.Activity)
admin.site.register(models.Attachment)
