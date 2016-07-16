import pytz
from django.db import models
from django.utils import timezone
from datetime import datetime
from .bandsintown import Client
from instaPhotoCollector.models import *
from googlemaps import Client as googleC, timezone as googleTZ
from instaPicXtractor import keys
from django.core.validators import MaxValueValidator, MinValueValidator

client = client = Client('myappid')
# https://github.com/jolbyandfriends/python-bandsintown


def parse_and_save_events(results):
    events = list()

    for result in results:
        event = Event.parse_and_save_data(result)
        events.append(event)

    return events


def get_time_zone_id(latitude, longitude):
    google_client = googleC(key=keys.timeZoneGetter_server_key)

    location = str(latitude) + "," + str(longitude)

    result = googleTZ.timezone(google_client, location)

    status = result['status']

    if status == "OK":
        time_zone_id = result['timeZoneId']
        return time_zone_id
    else:
        return None


def parse_as_tz_aware(dt_anaware, latitude, longitude):
    dt_object = datetime.strptime(dt_anaware, '%Y-%m-%dT%H:%M:%S')

    year = dt_object.year
    month = dt_object.month
    day = dt_object.day
    hour = dt_object.hour
    minute = dt_object.minute
    second = dt_object.second

    tz_id = get_time_zone_id(latitude, longitude)
    if not tz_id:
        return None

    tz = pytz.timezone(tz_id)

    dt_aware = tz.localize(datetime(year, month, day, hour, minute, second), is_dst=None)

    return dt_aware


class Artist(models.Model):
    facebook_page_url = models.CharField(max_length=511, null=True)
    upcoming_event_count = models.IntegerField(default=0)
    name = models.CharField(max_length=255)                         # PK
    tracker_count = models.IntegerField(default=0)
    mbid = models.CharField(max_length=255, null=True)
    image_url = models.CharField(max_length=511)
    facebook_tour_dates_url = models.CharField(max_length=511, null=True)
    thumb_url = models.CharField(max_length=511)

    def __unicode__(self):
        string = "Artist = %s" % self.name
        return string

    def is_stored(self):
        if Artist.objects.filter(name=self.name):
            return True
        else:
            return False

    @staticmethod
    def parse_and_save_data(a_json_obj):
        db_artist = Artist.objects.filter(name=a_json_obj['name'])

        if not db_artist:
            artist = Artist()
            artist.facebook_page_url = a_json_obj['facebook_page_url']
            artist.upcoming_event_count = a_json_obj['upcoming_event_count']
            artist.name = a_json_obj['name']
            artist.tracker_count = a_json_obj['tracker_count']
            artist.mbid = a_json_obj['mbid']
            artist.image_url = a_json_obj['image_url']
            artist.facebook_tour_dates_url = a_json_obj['facebook_tour_dates_url']
            artist.thumb_url = a_json_obj['thumb_url']

            artist.save()

            print 'log >>> artist saved on DB'
            """
            print artist.facebook_page_url
            print artist.upcoming_event_count
            print artist.name
            print artist.tracker_count
            print artist.mbid
            print artist.image_url
            print artist.facebook_page_url
            print artist.thumb_url
            #"""
            return artist
        else:
            print 'log >>> artist already on DB'
            return db_artist

    @staticmethod
    def find(artist_name):
        result = client.get(artist_name)

        return Artist.parse_and_save_data(result)

    def get_events_by_date(self, search_date):
        results = client.events(self.name, date=search_date)

        return parse_and_save_events(results)

    def get_events_by_dates_range(self, start_date, end_date):
        dates_range = "%s,%s" % (start_date, end_date)
        results = client.events(self.name, date=dates_range)

        return parse_and_save_events(results)

    def get_events_by_location(self, location):
        results = client.search(self.name, location=location)

        return parse_and_save_events(results)

    def get_events_by_location_and_radius(self, location, radius):
        # maximum radius value : 241 km (150 miles)
        if radius > 241:
            radius = 241
        results = client.search(self.name, location=location, radius=radius*0.621371)

        return parse_and_save_events(results)

    def get_recommended_events_by_location(self, location):
        results = client.recommended(self.name, location=location, only_recs=True)

        parsed_and_saved_events = parse_and_save_events(results)

        return parsed_and_saved_events

    def get_recommended_events_by_location_and_radius(self, location, radius):
        # maximum radius value : 241 km (150 miles)
        if radius > 241:
            radius = 241
        results = client.recommended(self.name, location=location, radius=radius*0.621371)

        parsed_and_saved_events = parse_and_save_events(results)

        return parsed_and_saved_events


class Venue(models.Model):
    city = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, null=True)
    region = models.CharField(max_length=255, null=True)
    longitude = models.FloatField(default=0, null=False)
    place = models.CharField(max_length=255)
    latitude = models.FloatField(default=0, null=False)

    def __unicode__(self):
        string = "Venue = %s [city:%s, latitude:%f, longitude:%f]" % (self.name, self.city, float(self.latitude),
                                                                      float(self.longitude))
        return string

    def is_stored(self):
        result = Venue.objects.filter(longitude=self.longitude, latitude=self.latitude)
        if result:
            return True
        else:
            return False

    @staticmethod
    def parse_and_save_data(v_json_obj):
        db_venue = Venue.objects.filter(longitude=(float(v_json_obj['longitude'])),
                                        latitude=(float(v_json_obj['latitude'])))

        if not db_venue:
            venue = Venue()
            venue.city = v_json_obj['city']
            venue.name = v_json_obj['name']
            venue.country = v_json_obj['country']
            venue.region = v_json_obj['region']
            venue.longitude = float(v_json_obj['longitude'])
            venue.place = v_json_obj['place']
            venue.latitude = float(v_json_obj['latitude'])

            venue.save()

            print 'log >>> venue saved on DB'
            """
            print venue.city
            print venue.name
            print venue.country
            print venue.region
            print venue.longitude
            print venue.place
            print venue.latitude
            #"""
            return venue
        else:
            print 'log >>> venue already on DB'
            return db_venue[0]


class Event(models.Model):
    description = models.CharField(max_length=1023, null=True)
    title = models.CharField(max_length=511)
    ticket_type = models.CharField(max_length=255, null=True)
    venue = models.ForeignKey('Venue')
    facebook_rsvp_url = models.CharField(max_length=511)
    ticket_url = models.CharField(max_length=511, null=True)
    on_sale_datetime = models.DateTimeField(null=True)
    formatted_datetime = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    formatted_location = models.CharField(max_length=255)
    artists = models.ManyToManyField(Artist)
    ticket_status = models.CharField(max_length=255)
    BIT_event_id = models.IntegerField()

    def __unicode__(self):
        string = "Event = %s" % self.title

        return string

    def is_stored(self):
        result = Event.objects.filter(BIT_event_id=self.BIT_event_id)
        if result:
            return True
        else:
            return False

    @staticmethod
    def parse_and_save_data(e_json_obj):
        db_event = Event.objects.filter(BIT_event_id=e_json_obj['id'])

        if not db_event:
            event = Event()

            event.description = e_json_obj['description']
            event.title = e_json_obj['title']
            event.ticket_type = e_json_obj['ticket_type']

            # parsing venue
            venue_json_obj = e_json_obj['venue']
            venue = Venue()
            venue = Venue.parse_and_save_data(venue_json_obj)
            event.venue = venue

            event.facebook_rsvp_url = e_json_obj['facebook_rsvp_url']
            event.ticket_url = e_json_obj['ticket_url']

            if (e_json_obj['on_sale_datetime']):
                event.on_sale_datetime = parse_as_tz_aware(e_json_obj['on_sale_datetime'],
                                                           venue.latitude, venue.longitude)
            else:
                event.on_sale_datetime = None

            event.formatted_datetime = e_json_obj['formatted_datetime']
            event.datetime = parse_as_tz_aware(e_json_obj['datetime'], venue.latitude, venue.longitude)
            event.formatted_location = e_json_obj['formatted_location']
            event.ticket_status = e_json_obj['ticket_status']
            event.BIT_event_id = e_json_obj['id']

            event.save()

            # extracting artists
            e_json_artists = e_json_obj['artists']

            for e_json_artist in e_json_artists:
                artist_name = e_json_artist['name']
                # searching in DB
                artist = Artist.objects.filter(name=artist_name).first()
                if not artist:
                    # searching on BIT
                    artist = Artist.find(artist_name)
                    artist.save()
                # adding artist to event artists
                event.artists.add(artist)

            print 'log >>> event saved on DB'
            """
            print event.description
            print event.title
            print event.ticket_type
            print event.venue
            print event.facebook_rsvp_url
            print event.ticket_url
            print event.on_sale_datetime
            print event.formatted_datetime
            print event.datetime
            print event.formatted_location
            print event.ticket_status
            print event.BIT_event_id
            #"""
            return event
        else:
            print 'log >>> event already on DB'
            return db_event[0]

    def get_media_count(self):
        return Media.objects.filter(event=self.id).count()


class RecommendedEvents(models.Model):
    event = models.ForeignKey(Event, related_name='main_event')
    radius = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(241)])
    events = models.ManyToManyField(Event, related_name='recommended_events')
