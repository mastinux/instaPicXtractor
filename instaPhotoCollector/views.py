from django.shortcuts import render
from django.http import HttpResponse
from instagram.client import InstagramAPI
from django.template import loader
from django.utils import timezone
import time
from django.utils.timezone import timedelta
from datetime import timedelta as std_timedelta
from models import *
from BITdataCollector.bandsintown import Client
from BITdataCollector.models import *
from instaPicXtractor import keys
from IdataCollector.views import Authentication
from ast import literal_eval
import hmac
from hashlib import sha256
import urllib
import requests

# todo : integrate photo_swipe
# http://photoswipe.com/documentation/getting-started.html
# compiled files are in static/photo_swipe/PhotoSwipe/dist

client = Client('myappid')

I_API_URL = "https://api.instagram.com/v1/"
USERS_SELF = "users/self/"
USERS_SELF_MEDIA_RECENT = "users/self/media/recent/"
USERS_SELF_MEDIA_LIKED = "users/self/media/liked"

INIT_DAYS_FOR_LAST_ARTIST_EVENTS = 30*2
UPDATE_DAYS_FOR_LAST_ARTIST_EVENTS = 30
EVENT_PER_PAGE = 7
MEDIA_PER_PAGE = 20
DAYS_FOR_LAST_ARTIST_EVENTS = 30*2

interesting_artists = ['Katy Perry', 'Hozier', 'Maroon 5', 'Coldplay',
                       'Rae Sremmurd', 'James Bay', 'Linkin Park', 'System of a Down',
                       'Years & Years', 'Mark Ronson', 'DAYA', 'Glass Animals', 'All Time Low',
                       'Taylor Swift', 'Ariana Grande',
                       'KITTENS', 'Run The Jewels', 'The Accidentals', 'Fetty Wap',  'George Ezra',
                       ]

api = InstagramAPI(client_id=keys.INSTAGRAM_CLIENT_ID,
                   client_secret=keys.INSTAGRAM_CLIENT_SECRET)


def access_token_curl_request(code):
    params = dict()
    params['client_id'] = keys.INSTAGRAM_CLIENT_ID
    params['client_secret'] = keys.INSTAGRAM_CLIENT_SECRET
    params['grant_type'] = 'authorization_code'
    params['redirect_uri'] = keys.INSTAGRAM_REDIRECT_URI
    params['code'] = code
    # scope=public_content
    params['scope'] = 'public_content'

    params = urllib.urlencode(params)
    feed = urllib.urlopen("https://api.instagram.com/oauth/access_token", params)
    oauth_token = feed.read()

    return literal_eval(oauth_token)


def generate_sig(endpoint, params, secret):
    sig = endpoint
    for key in sorted(params.keys()):
        sig += '|%s=%s' % (key, params[key])
    print sig
    return hmac.new(secret, sig, sha256).hexdigest()


# TODO: test again this function after being able to make proper request to the API
# check Security tab in Edit Client from Manage Clients
def sig_curl_request(endpoint, internal_params, access_token):
    params = dict()

    sig = generate_sig(endpoint, internal_params, keys.INSTAGRAM_CLIENT_SECRET)

    params['access_token'] = access_token
    params['sig'] = sig

    params = urllib.urlencode(params)
    feed = urllib.urlopen("https://api.instagram.com/v1" + endpoint, params)
    result = feed.read()

    return result


def get_users_self(access_token):
    params = dict()

    params['access_token'] = access_token

    response = requests.get(I_API_URL + USERS_SELF, params=params)

    result = response.json()

    if result['meta']['code'] != 200:
        return None
    else:
        return result['data']


# TODO: if necessary manage pagination
def get_users_self_media_recent(access_token):
    params = dict()

    params['access_token'] = access_token

    response = requests.get(I_API_URL + USERS_SELF_MEDIA_RECENT, params=params)

    result = response.json()

    if result['meta']['code'] != 200:
        return None
    else:
        return result['data']


def index(request):

    return render(request, 'instaPhotoCollector/base.html')


def search(request):
    context = {}
    if request.method == 'POST':
        image_objects = list()

        searched_tag = request.POST.get('searched_tag')

        print ">>> searched tag", searched_tag

        response = api.tag_recent_media(100, 0, searched_tag)
        media = response[0]

        for m in media:
            image = {}
            image['image_url'] = m.images['standard_resolution'].url

            image_objects.append(image)

        context = {
            'image_objects': image_objects,
        }
    return render(request, 'instaPhotoCollector/index.html', context)


def popular(request):
    image_objects = list()

    """
    media = api.media_popular(count=10)
    for m in media:
        print m

    for m in media:
        image = {}
        image['image_url'] = m.images['standard_resolution'].url

        image_objects.append(image)
    """
    context = {
        'image_objects': image_objects,
    }

    return render(request, 'instaPhotoCollector/index.html', context)


def search_by_location(request):
    context = {}

    if request.method == 'POST':
        image_objects = list()

        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')

        start = timezone.now() - timezone.timedelta(days=14)
        end = timezone.now() - timezone.timedelta(days=7)

        start_epoch = int(time.mktime(start.timetuple()))
        end_epoch = int(time.mktime(end.timetuple()))

        # todo: understand what's first parameter for api.media_search()
        media = api.media_search('', 100, lat, lng, start_epoch, end_epoch)

        for m in media:
            image = {}
            image['location'] = m.location
            image['created_time'] = m.created_time
            image['tags'] = m.tags
            image['image_url'] = m.images['standard_resolution'].url

            image_objects.append(image)

        context = {
            'image_objects': image_objects
        }

    return render(request, 'instaPhotoCollector/index.html', context)


def get_artists(request):
    # todo : add description for number of events for each artist
    artist_objects = list()
    context = {}

    """
    db_artists = Artist.objects.filter(name__in=interesting_artists)

    for DB_artist in db_artists:
        artist_objects.append(DB_artist)
        if interesting_artists.__contains__(DB_artist.name):
            interesting_artists.remove(DB_artist.name)

    for artist_name in interesting_artists:
        result = client.get(artist_name)
        artist = Artist()
        artist.parse_data(result)
        if not artist.is_stored():
            artist.save()
        artist_objects.append(artist)
    """
    artist_objects = Artist.objects.all()
    context['artist_objects'] = artist_objects

    return render(request, 'instaPhotoCollector/artists.html', context)


def explore_artist(request, artist_name, page):
    context = dict()
    context['artist_name'] = artist_name

    artist = Artist.objects.get(name=artist_name)
    """
    end = timezone.now()
    start = end - timedelta(days=DAYS_FOR_LAST_ARTIST_EVENTS)
    artist.get_events_by_dates_range(start.date(), end.date())
    """
    db_artist_events = artist.event_set.filter(datetime__lt=timezone.now()).order_by('-datetime')

    number_of_element = db_artist_events.count()
    if number_of_element > 0:
        number_of_pages = number_of_element / EVENT_PER_PAGE
        if number_of_element % EVENT_PER_PAGE != 0:
            number_of_pages += 1

        start_number = (int(page) - 1) * EVENT_PER_PAGE
        end_number = int(page) * EVENT_PER_PAGE

        context['artist_events'] = db_artist_events[start_number:end_number]
        context['range'] = range(1, number_of_pages + 1)
        context['first_page'] = 1
        context['page'] = page
        context['last_page'] = number_of_pages

    # TODO : set recommended events search after user click
    # FIXME : recommended events are future events, exploit artists of recommended events

    recommended_events = list()
    """
    for db_artist_event in db_artist_events:
        print ">>> retrieving recommended events for ", db_artist_event.title
        #print db_artist_event.venue.city
        #print db_artist_event.venue.country
        #print db_artist_event.venue.region
        location = db_artist_event.formatted_location
        print location

        partial_recommended_events = artist.get_recommended_events_by_location(location)
        recommended_events.append(partial_recommended_events)

        city = db_artist_event.venue.city
        region = db_artist_event.venue.region

        if not (
                city is None
                or "." in city
                or not city.isalpha()
                or region is None
                or "." in region
                or not region.isalpha()
                ):
            location = city + "," + region
            print location

            # TODO : encapsulate BIT request in try structure
            partial_recommended_events = artist.get_recommended_events_by_location(location)

            if isinstance(partial_recommended_events, list):
                print type(partial_recommended_events)
                for e in partial_recommended_events:
                    print type(e)
                    for ee in e:
                        print type(ee)
                        print ee
                        recommended_events.append(ee)
            else:
                print "TODO : analyze partial recommended events type"
        """

    if recommended_events:
        context['recommended_events'] = recommended_events
    else:
        print "no recommended events found"

    return render(request, 'instaPhotoCollector/artist.html', context)


def explore_event(request, event_id, page):
    context = {}
    image_objects = list()
    retrieved_tags = list()

    event = Event.objects.get(id=event_id)

    # fixme : instagram query search for given date and place by our time zone, make time zone aware

    event_medias = Media.objects.filter(event=event_id)

    if event_medias.count() == 0:
        print " >>> retrieving images for event", event.id
        for e in event.title.replace(",", " ").replace("@", " ").split():
            retrieved_tags.append(e.lower())
        #main_tag = retrieved_tags[0]
        #retrieved_tags.remove(main_tag)

        lat = event.venue.latitude
        lng = event.venue.longitude

        start = event.datetime - std_timedelta(hours=12)
        end = event.datetime + std_timedelta(hours=12)

        start_epoch = int(time.mktime(start.timetuple()))
        end_epoch = int(time.mktime(end.timetuple()))

        # todo: understand what's first parameter for api.media_search()
        medias = api.media_search('', 1000, lat, lng, start_epoch, end_epoch)

        for media in medias:
            #if main_tag in [mt.name for mt in medium.tags]:
                if [mt for mt in media.tags if mt.name in retrieved_tags]:
                    #print "\n", media.tags
                    db_media = Media.objects.filter(instagram_id=media.id)
                    if not db_media:
                        media_object = Media()
                        media_object.instagram_id = media.id
                        media_object.std_resolution_url = media.images['standard_resolution'].url
                        media_object.low_resolution_url = media.images['low_resolution'].url
                        media_object.thumbnail_url = media.images['thumbnail'].url
                        media_object.location = media.location
                        if media.location.point:
                            media_object.longitude = media.location.point.longitude
                            media_object.latitude = media.location.point.latitude
                        media_object.created_time = media.created_time
                        media_object.like_count = media.like_count
                        media_object.event = event_id
                        media_object.save()
                        #print media_object

        event_medias = Media.objects.filter(event=event_id)
    else:
        print " >>> images for event", event.id, "already on DB"

    number_of_element = event_medias.count()
    print " >>> retrieved", number_of_element, "images"
    number_of_pages = number_of_element / MEDIA_PER_PAGE
    if number_of_element % MEDIA_PER_PAGE != 0:
        number_of_pages += 1

    start_number = (int(page) - 1) * MEDIA_PER_PAGE
    end_number = int(page) * MEDIA_PER_PAGE

    event_medias = event_medias[start_number:end_number]

    for event_media in event_medias:
        image = {}
        image['image_url'] = event_media.std_resolution_url

        image_objects.append(image)

    context['event_id'] = event_id
    context['event_title'] = event.title
    context['image_objects'] = image_objects

    context['range'] = range(1, number_of_pages + 1)
    context['first_page'] = 1
    context['page'] = page
    context['last_page'] = number_of_pages

    return render(request, 'instaPhotoCollector/event.html', context)


def init_db(request):
    # retrieve artists data
    for artist_name in interesting_artists:
        print "processing data for", artist_name
        result = client.get(artist_name)
        artist = Artist()
        artist.parse_data(result)
        if not artist.is_stored():
            artist.save()

    artists = Artist.objects.all()
    end = timezone.now()
    start = end - timedelta(days=INIT_DAYS_FOR_LAST_ARTIST_EVENTS)

    # retrieving artists events data
    for a in artists:
        print "processing event for", artist.name
        a.get_events_by_dates_range(start.date(), end.date())

    return render(request, 'instaPhotoCollector/index.html')


def update_artists(request):
    artists = Artist.objects.all()

    # update data for all artists
    for artist in artists:
        print "old data for", artist.name
        result = client.get(artist.name)
        tmp_artist = Artist()
        tmp_artist.parse_data(result)
        tmp_artist.id = artist.id
        print "new data for", artist.name
        tmp_artist.save()

    return render(request, 'instaPhotoCollector/index.html')


def retrieve_artists_events(request):
    artists = Artist.objects.filter(name__in=interesting_artists)
    end = timezone.now()
    start = end - timedelta(days=UPDATE_DAYS_FOR_LAST_ARTIST_EVENTS)

    for a in artists:
        print a
        a.get_events_by_dates_range(start.date(), end.date())

    return render(request, 'instaPhotoCollector/index.html')


def retrieve_all_events_media(request):
    artists = Artist.objects.filter(name__in=interesting_artists)
    artists_ids = [a.id for a in artists]

    for event in Event.objects.filter(datetime__lt=timezone.now(), artists__in=artists_ids
            #, id__gt=1086
                                      ):
        if not Media.objects.filter(event=event.id):
            print "log >>> processing event", event.title
            retrieved_tags = list()

            for e in event.title.replace(",", " ").replace("@", " ").split():
                retrieved_tags.append(e.lower())

            lat = event.venue.latitude
            lng = event.venue.longitude

            start = event.datetime - std_timedelta(hours=3)
            end = event.datetime + std_timedelta(hours=15)

            start_epoch = int(time.mktime(start.timetuple()))
            end_epoch = int(time.mktime(end.timetuple()))

            medias = api.media_search('', 1000, lat, lng, start_epoch, end_epoch)

            for media in medias:
                #if main_tag in [mt.name for mt in medium.tags]:
                    if [mt for mt in media.tags if mt.name in retrieved_tags]:
                        #print "\n", media.tags
                        db_media = Media.objects.filter(instagram_id=media.id)
                        if not db_media:
                            media_object = Media()
                            media_object.instagram_id = media.id
                            media_object.std_resolution_url = media.images['standard_resolution'].url
                            media_object.low_resolution_url = media.images['low_resolution'].url
                            media_object.thumbnail_url = media.images['thumbnail'].url
                            media_object.location = media.location
                            if media.location.point:
                                media_object.longitude = media.location.point.longitude
                                media_object.latitude = media.location.point.latitude
                            media_object.created_time = media.created_time
                            media_object.like_count = media.like_count
                            media_object.event = event.id
                            media_object.save()

    return render(request, 'instaPhotoCollector/index.html')


def test(request):
    context = {}

    authentication = Authentication()
    context['authorization_url'] = authentication.get_authorization_url()

    return render(request, 'instaPhotoCollector/test.html', context)


def test_2(request):
    context = {}

    error = request.GET.get('error', '')
    error_reason = request.GET.get('error_reason', '')
    error_description = request.GET.get('error_description', '')

    if error == "access_denied":
        context['msg'] = "You denied the authorization to our application."

        authentication = Authentication()
        context['authorization_url'] = authentication.get_authorization_url()

        return render(request, 'instaPhotoCollector/test.html', context)

    code = request.GET.get('code', '')

    oauth_token = access_token_curl_request(code)

    #"""
    access_token = oauth_token["access_token"]
    """
    user_username = oauth_token['user']['username']
    user_bio = oauth_token['user']['bio']
    user_website = oauth_token['user']['website']
    user_profile_picture = oauth_token['user']['profile_picture']
    user_full_name = oauth_token['user']['full_name']
    user_id = oauth_token['user']['id']
    """

    """
    print access_token
    print user_username
    print user_bio
    print user_website
    print user_profile_picture
    print user_full_name
    print user_id
    #"""

    # result = get_users_self(access_token)

    """
    user_counts = result['counts']
    user_media = user_counts['media']
    user_followed_by = user_counts['followed_by']
    user_follows = user_counts['follows']
    #"""
    """
    print user_media
    print user_followed_by
    print user_follows
    #"""

    # results = get_users_self_media_recent(access_token)

    """
    for image_object in results:
        print
        # print image_object
        user_has_liked = image_object['user_has_liked']
        attribution = image_object['attribution']
        tags = image_object['tags']
        user_object = image_object['user']
        comments_count = image_object['comments']['count']
        filter = image_object['filter']
        images = image_object['images']
        # 320 x 320
        low_resolution_url = images['low_resolution']['url']
        # 150 x 150
        thumbnail_url = images['thumbnail']['url']
        # 640 x 640
        standard_resolution_url = images['standard_resolution']['url']
        link = image_object['link']
        location = image_object['location']
        created_time = image_object['created_time']
        users_in_photo = image_object['users_in_photo']
        caption = image_object['caption']
        type = image_object['type']
        id = image_object['id']
        likes_count = image_object['likes']['count']
    #"""
    """
        print user_has_liked
        print attribution
        for tag in tags:
            print tag
        print user_object
        print comments_count
        print filter
        # print images
        print low_resolution_url
        print thumbnail_url
        print standard_resolution_url
        print link
        print location
        print created_time
        print users_in_photo
        print caption
        print type
        print id
        print likes_count
    #"""

    context['msg'] = "Access token get."

    return render(request, 'instaPhotoCollector/test_authorized.html', context)
