from django.shortcuts import render
from django.http import HttpResponse
from instagram.client import InstagramAPI
from django.template import loader
from django.utils import timezone
import time


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
            #print medium.location
            image['location'] = medium.location
            #print medium.created_time
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