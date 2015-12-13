from django.shortcuts import render
from django.http import HttpResponse
from .bandsintown import Client
from .models import *
import json


def index(request):
    client = Client('myappid')
    artists_names = ['Usher', 'Cage the Elephant', 'Martin Garrix', 'Knife Party', 'Steve Aoki']

    #for artist_name in artists_names:
    #    result = client.get(artist_name)
    #    artist = Artist()
    #    artist.parse_data(result)
    #    artist.save()
    #for a in Artist.objects.all():
    #    print a
    venues = Venue.objects.all()
    #for v in venues:
    #    v.delete()
    events = Event.objects.all()
    for e in events:
        e.delete()

    for artist in Artist.objects.all():
        results = client.events(artist.name)
        for result in results:
            event = Event()
            event.parse_data(result)
    #events = client.events('Knife Party', date='2015-01-31,2015-12-31')


    return HttpResponse("Hello, world. You're at the index.")
