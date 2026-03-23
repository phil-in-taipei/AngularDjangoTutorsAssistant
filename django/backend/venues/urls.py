from django.urls import path

from .views import VenueSpacesByVenueViewSet


app_name = 'venues'
urlpatterns = [
    path(
        'spaces/by-venue/', VenueSpacesByVenueViewSet.as_view(),
        name='spaces-by-venue'
    ), #<int:venue_id>/
]
