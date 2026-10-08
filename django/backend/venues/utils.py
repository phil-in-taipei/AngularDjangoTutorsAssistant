from .models import VenueSpace


def get_available_spaces_at_venue(venue, booked_spaces):
    """
    Return the VenueSpaces at `venue` that are not in `booked_spaces`.

    Args:
        venue: a Venue instance.
        booked_spaces: an iterable of VenueSpace instances (or a QuerySet)
            that are already booked for the time period in question.

    Returns:
        A list of VenueSpace instances at `venue` that are still available.
    """
    booked_ids = {space.pk for space in booked_spaces}

    return list(
        VenueSpace.objects.filter(venue=venue).exclude(pk__in=booked_ids)
    )
