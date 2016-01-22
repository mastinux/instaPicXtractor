from django.shortcuts import render
from django.http import HttpResponse
from instagram.client import InstagramAPI
from django.template import loader
from django.utils import timezone
import time
from django.utils.timezone import timedelta
from datetime import timedelta as std_timedelta
# BITdataCollector modules
from BITdataCollector.bandsintown import Client
from BITdataCollector.models import *


client = Client('myappid')


def index(request):
    # todo : combine BITdataCollector with instaPhotoCollector

    return render(request, 'instaPhotoCollector/base.html')


def search(request):
    context = {}
    if request.method == 'POST':
        api = InstagramAPI(client_id='f72f37aa491541a79412ce319f2e061f',
                           client_secret='7dba20c9e90b4758b558088f9422cadd')
        image_objects = list()

        searched_tag = request.POST.get('searched_tag')

        print ">>> tag searched", searched_tag

        response = api.tag_recent_media(40, 0, searched_tag)
        media = response[0]

        for medium in media:
            image = {}
            #for e in medium.__dict__:
            #    print e
            #for e in api.media(medium.id).__dict__:
            #    print e
            image['image_url'] = medium.images['standard_resolution'].url

            image_objects.append(image)

        context = {
            'image_objects': image_objects,
        }
    return render(request, 'instaPhotoCollector/index.html', context)


def popular(request):
    api = InstagramAPI(client_id='f72f37aa491541a79412ce319f2e061f', client_secret='7dba20c9e90b4758b558088f9422cadd')
    image_objects = list()

    media = api.media_popular(count=20)
    for medium in media:
        image = {}
        #print "\n"
        #for e in medium.__dict__:
        #    print e
        image['image_url'] = medium.images['standard_resolution'].url

        image_objects.append(image)

    context = {
        'image_objects': image_objects,
    }
    return render(request, 'instaPhotoCollector/index.html', context)


def search_by_location(request):
    context = {}
    if request.method == 'POST':
        api = InstagramAPI(client_id='f72f37aa491541a79412ce319f2e061f',
                           client_secret='7dba20c9e90b4758b558088f9422cadd')
        image_objects = list()

        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')

        start = timezone.now() - timezone.timedelta(days=14)
        end = timezone.now() - timezone.timedelta(days=7)

        start_epoch = int(time.mktime(start.timetuple()))
        end_epoch = int(time.mktime(end.timetuple()))

        # todo: understand what's first parameter for api.media_search()
        media = api.media_search('', 20, lat, lng, start_epoch, end_epoch)

        for medium in media:
            image = {}
            print "\n"
            #for e in medium.__dict__:
            #    print e
            #print medium.caption
            print medium.location
            image['location'] = medium.location
            print medium.created_time
            image['created_time'] = medium.created_time
            #print medium.tags
            image['tags'] = medium.tags
            #print medium.comments
            #print medium.filter
            #print medium.comment_count
            #print medium.like_count
            #print medium.link
            #print medium.likes
            #print medium.images
            #print medium.users_in_photo
            #print medium.type
            #print medium.id
            #print medium.user
            image['image_url'] = medium.images['standard_resolution'].url

            image_objects.append(image)

        context = {
            'image_objects': image_objects
        }
    return render(request, 'instaPhotoCollector/index.html', context)


def retrieve_artists(request):
    # todo : combine BITdataCollector with instaPhotoCollector
    artists = ['Rae Sremmurd', 'James Bay', 'Hozier',
               # 'Years & Years', 'Mark Ronson', 'DAYA', 'Glass Animals', 'All Time Low', 'System of a Down',
               # 'George Ezra',
               'KITTENS', 'Run The Jewels', 'The Accidentals', 'Fetty Wap']
    artist_objects = list()
    context = {}

    DB_artists = Artist.objects.filter(name__in=artists)
    for DB_artist in DB_artists:
        artist_objects.append(DB_artist)
        if artists.__contains__(DB_artist.name):
            artists.remove(DB_artist.name)

    for artist_name in artists:
        result = client.get(artist_name)
        artist = Artist()
        artist.parse_data(result)
        if not artist.is_stored():
            artist.save()
        artist_objects.append(artist)

    context = {
        'artist_objects': artist_objects
    }

    return render(request, 'instaPhotoCollector/artists.html', context)


def explore_artist(request):
    context = {}

    if request.method == 'POST':
        artist_name = request.POST.get('artist_name')
        context['artist_name'] = artist_name
        artist = Artist.objects.get(name=artist_name)

        # search events in last 30 days on BIT (stored automatically)
        start = timezone.now() - timedelta(days=30)
        end = timezone.now()
        artist_events = artist.get_events_by_dates_range(start.date(), end.date())

        DB_artist_events = artist.event_set.all().order_by('-datetime')

        context['artist_events'] = DB_artist_events

    return render(request, 'instaPhotoCollector/artist.html', context)


def explore_event(request, event_id):
    image_objects = list()
    retrieved_tags = list()

    event = Event.objects.get(id=event_id)

    for e in event.title.replace(",", " ").replace("@", " ").split():
        retrieved_tags.append(e.lower())
    #main_tag = retrieved_tags[0]
    #retrieved_tags.remove(main_tag)

    api = InstagramAPI(client_id='f72f37aa491541a79412ce319f2e061f',
                       client_secret='7dba20c9e90b4758b558088f9422cadd')

    lat = event.venue.latitude
    lng = event.venue.longitude

    start = event.datetime - std_timedelta(hours=6)
    end = event.datetime + std_timedelta(hours=6)

    start_epoch = int(time.mktime(start.timetuple()))
    end_epoch = int(time.mktime(end.timetuple()))

    # todo: understand what's first parameter for api.media_search()
    media = api.media_search('', 500, lat, lng, start_epoch, end_epoch)

    for medium in media:
        #if main_tag in [mt.name for mt in medium.tags]:
            if [mt for mt in medium.tags if mt.name in retrieved_tags]:
                # todo : save medium in database
                image = {}
                image['location'] = medium.location
                image['created_time'] = medium.created_time
                image['tags'] = medium.tags
                image['image_url'] = medium.images['standard_resolution'].url

                image_objects.append(image)

    context = {
        'image_objects': image_objects
    }

    return render(request, 'instaPhotoCollector/index.html', context)
