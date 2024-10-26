"""URL configuration for activities app."""
from django.urls import path, include
from . import views

app_name = "activities"
urlpatterns = [
    path("", views.ActivityList.as_view(), name="index"),
    path("<int:pk>/", views.ActivityDetail.as_view(), name="detail"),
    path("join/<int:pk>/", views.JoinLeaveView.as_view(), name="join"),

    # Utilities.
    path('get-csrf-token/', views.util.csrf_token_view, name='get_csrf_token'),
    path('get-participant/<int:activity_id>/', views.util.get_participant_detail, name='get_participant'),
    path('get-recently/', views.util.get_recent_activity, name='get_recently')
]