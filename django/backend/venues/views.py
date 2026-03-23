from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Venue, VenueSpace
from .serializers import VenueSpaceGoogleSheetsSerializer


# note: this is a temporary setup that will be replaced after teachers
# and Venue spaces have many-to-many database relationships
# Api calls will be made on behalf of teachers to get venue spaces
# for the venues which they are 'members' of
class VenueSpacesByVenueViewSet(generics.ListAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    queryset = VenueSpace.objects.all()
    serializer_class = VenueSpaceGoogleSheetsSerializer
    lookup_field = 'id'
    model = serializer_class.Meta.model

    def get_queryset(self):
        #venue_id = self.kwargs.get("venue_id")
        #queryset = self.model.objects.filter(venue__id=venue_id)
        queryset = self.queryset = self.model.objects.all()
        return queryset.order_by('space_name')
