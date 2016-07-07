from django.shortcuts import render
from django.http import HttpResponse
from bandsintown import Client
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

    client = Client('myappid')
    artists_names = ['Usher', 'Cage the Elephant', 'Knife Party', 'Steve Aoki', 'Lady Gaga', 'The Weeknd', 'Rihanna']
    #artists_names = ['Rihanna']

    #todo: test all methods in models

    for name in artists_names:
        Artist.find(name)

    for a in Artist.objects.all():
        print a


    return HttpResponse("Hi, you are in BITdataCollector.")
