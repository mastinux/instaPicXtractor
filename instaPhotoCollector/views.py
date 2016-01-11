from django.shortcuts import render
from django.http import HttpResponse
from instagram.client import InstagramAPI
from django.template import loader
from django.utils import timezone
import time


def index(request):
    # todo: understand what's first parameter for api.media_search()

    api = InstagramAPI(client_id='f72f37aa491541a79412ce319f2e061f', client_secret='7dba20c9e90b4758b558088f9422cadd')
    images_url = list()
    """
    #SEARCH POPULAR
    media = api.media_popular(count=20)
    for medium in media:
        images_url.append(medium.images['standard_resolution'].url)
    """
    """
    #SEARCH BY LOCATION AND TIME
    start = timezone.now() - timezone.timedelta(days=18)
    end = timezone.now() - timezone.timedelta(days=16)

    start_epoch = int(time.mktime(start.timetuple()))
    end_epoch = int(time.mktime(end.timetuple()))

    media = api.media_search('', 20, 40.716667, -74, start_epoch, end_epoch)

    for medium in media:
        print "\n"
        #for e in medium.__dict__:
        #    print e
        #print medium.caption
        print medium.location
        print medium.created_time
        #print medium.tags
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
        images_url.append(medium.images['standard_resolution'].url)
    """

    # SEARCH BY TAG
    response = api.tag_recent_media(40, 0, 'roma')
    media = response[0]

    for medium in media:
        #for e in medium.__dict__:
        #    print e
        #for e in api.media(medium.id).__dict__:
        #    print e
        images_url.append(medium.images['standard_resolution'].url)

    context = {
        'images_url': images_url,
    }
    return render(request, 'instaPhotoCollector/index.html', context)
