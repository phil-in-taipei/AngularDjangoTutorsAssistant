from rest_framework import serializers

from .models import Venue, VenueSpace


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = "__all__"


class VenueGoogleSheetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = (
            'id', 'venue_name',
        )


class VenueSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueSpace
        fields = "__all__"


class VenueSpaceGoogleSheetsSerializer(serializers.ModelSerializer):
    venue = VenueGoogleSheetsSerializer(read_only=True)

    class Meta:
        model = VenueSpace
        fields = (
            'id', 'space_name', 'venue',
            'number_of_seats',
        )