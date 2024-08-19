from django.urls import path

from apps.logic.views import NewRatingView

app_name = 'logic'
urlpatterns = [
    path("rating/<user_uuid>", NewRatingView.as_view(), name="new-rating"),
]
