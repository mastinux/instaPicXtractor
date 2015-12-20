from django.shortcuts import render
from django.http import HttpResponse
from .bandsintown import Client
from .models import *
from django.utils.timezone import timedelta


def index(request):
    client = Client('myappid')
    artists_names = ['Usher', 'Cage the Elephant', 'Knife Party', 'Steve Aoki', 'Lady Gaga', 'The Weeknd']

    #TEST : artists search
    for artist_name in artists_names:
        result = client.get(artist_name)
        artist = Artist()
        artist.parse_data(result)
        if not artist.exists():
            print "... saving ", artist
            artist.save()
    """
    for a in Artist.objects.all():
        a.delete()
        print a

    for v in Venue.objects.all():
        v.delete()
        print v

    for e in Event.objects.all():
        e.delete()
        print e

    #TEST : events search
    for artist in Artist.objects.all():
        results = client.events(artist.name)
        for result in results:
            event = Event()
            event.parse_and_save_data(result)
            #event.save()
    """

    artist = Artist.objects.filter(name='The Weeknd').first()
    start = timezone.now() - timedelta(days=12)
    end = timezone.now()

    #TEST : search artist event by date
    print artist.get_event_by_date(start.date())

    #TEST : search artist events by dates range
    for e in artist.get_events_by_dates_range(start.date(), end.date()):
        print e

    return HttpResponse("Hi, here the hell begins.")
