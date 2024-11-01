"""URL configuration for activities app."""
from django.urls import path
from . import views

app_name = "activities"
urlpatterns = [
    path("", views.ActivityList.as_view(), name="index"),
    path("<int:pk>/", views.ActivityDetail.as_view(), name="detail"),
    path("join/<int:pk>/", views.JoinLeaveView.as_view(), name="join"),
    path("check-in/<int:pk>/", views.CheckInView.as_view(), name="checkin"),

    # Utilities.
    path('get-csrf-token/', views.util.csrf_token_view, name='get_csrf_token'),
    path('get-recently/', views.util.get_recent_activity, name='get_recently')
]
