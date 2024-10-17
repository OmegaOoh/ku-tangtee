"""URL configuration for activities app."""
from django.urls import path, include
from . import views
from . import old_views

app_name = "activities"
urlpatterns = [
    path("", views.ActivityList.as_view(), name="index"),
    path("<int:activity_id>/join", old_views.join, name="join"),
    path("<int:pk>", views.ActivityDetail.as_view(), name="detail"),
    # path("create", views.create, name="create"),
    path("<int:activity_id>/edit", old_views.edit_activity, name="edit_activity"),
    
    # Utilities.
    path('get-csrf-token/', views.util.csrf_token_view , name='get_csrf_token'),
    path('get-timezone/', views.util.get_timezone, name='get_timezone')
]
