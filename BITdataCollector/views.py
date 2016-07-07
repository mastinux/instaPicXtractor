from django.http import HttpResponse
from models import Artist, Venue, Event
from django.utils import timezone
from datetime import timedelta


def index(request):
    print "purging"
    for e in Event.objects.all():
        e.delete()

    for v in Venue.objects.all():
        v.delete()

    for a in Artist.objects.all():
        a.delete()
    print "purged"

    #artists_names = ['Usher', 'Cage the Elephant', 'Knife Party', 'Steve Aoki', 'Lady Gaga', 'The Weeknd', 'Rihanna']
    artists_names = ['Rihanna']

    for name in artists_names:
        Artist.find(name)

    start = timezone.now() + timedelta(days=0)
    end = timezone.now() + timedelta(days=7)
    for a in Artist.objects.all():
        a.get_events_by_dates_range(start.date(), end.date())

    return HttpResponse("Hi, you are in BITdataCollector.")
