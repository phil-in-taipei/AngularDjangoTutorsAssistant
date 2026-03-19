from rest_framework import serializers

from .models import Venue, VenueSpace


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = "__all__"


class VenueSpaceSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(read_only=True)

    class Meta:
        model = VenueSpace
        fields = (
            'id', 'space_name', 'venue',
            'number_of_seats',
        )