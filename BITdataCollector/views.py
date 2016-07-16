from django.http import HttpResponse
from models import Artist, Venue, Event
from django.utils import timezone
from datetime import timedelta


def index(request):
    #"""
    print "purging"
    for e in Event.objects.all():
        e.delete()

    for v in Venue.objects.all():
        v.delete()

    for a in Artist.objects.all():
        a.delete()
    print "purged"

    artists_names = ['Usher', 'Cage the Elephant', 'Knife Party', 'Steve Aoki', 'The Weeknd', 'Rihanna']
    # artists_names = ['Rihanna']

    for name in artists_names:
        Artist.find(name)
    #"""

    start = timezone.now() - timedelta(days=7)
    end = timezone.now() + timedelta(days=0)

    for artist in Artist.objects.all():
        events = artist.get_events_by_dates_range(start.date(), end.date())
        for event in events:
            lat = event.venue.latitude
            lng = event.venue.longitude
            recommended_events = artist.get_recommended_events_by_location_and_radius(str(lat) + "," + str(lng), 100)
            if recommended_events:
                print "Recommended event for ", event
                for e in recommended_events:
                    print e

    # TODO: save recommended events in a proper way

    return HttpResponse("Hi, you are in BITdataCollector.")
