from django.db import models
from django.utils import timezone
from .bandsintown import Client
from instaPhotoCollector.models import *

client = client = Client('myappid')
# https://github.com/jolbyandfriends/python-bandsintown


def parse_and_save_events(results):
    events = list()

    for result in results:
        event = Event.parse_and_save_data(result)
        events.append(event)

    return events


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

        artist = Artist.parse_and_save_data(result)

        return artist

    def get_events_by_date(self, search_date):
        results = client.events(self.name, date=search_date)

        return parse_and_save_events(results)

    def get_events_by_dates_range(self, start_date, end_date):
        dates_range = "%s,%s" % (start_date, end_date)
        results = client.events(self.name, date=dates_range)

        return parse_and_save_events(results)

    def get_events_by_location(self, location_name):
        results = client.search(self.name, location=location_name)

        return parse_and_save_events(results)

    def get_events_by_location_and_radius(self, location_name, radius):
        # maximum radius value : 241 km (150 miles)
        if radius > 241:
            radius = 241
        results = client.search(self.name, location=location_name, radius=radius*0.621371)

        return parse_and_save_events(results)

    def get_recommended_events_by_location(self, location):
        results = client.recommended(self.name, location=location, only_recs=True)

        return parse_and_save_events(results)

    def get_recommended_events_by_location_and_radius(self, location_name, radius):
        # maximum radius value : 241 km (150 miles)
        if radius > 241:
            radius = 241
        results = client.recommended(self.name, location=location_name, radius=radius*0.621371)

        return parse_and_save_events(results)


class Venue(models.Model):
    city = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, null=True)
    region = models.CharField(max_length=255, null=True)
    longitude = models.FloatField(default=0, null=False)
    place = models.CharField(max_length=255)
    latitude = models.FloatField(default=0, null=False)

    def __unicode__(self):
        string = "Venue = %s [city:%s, latitude:%f, longitude:%f]" % (self.name, self.city,
                                                                      self.latitude, self.longitude)
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
            return db_venue


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

            venue_json_obj = e_json_obj['venue']
            venue = Venue.parse_and_save_data(venue_json_obj)
            # assigning venue
            event.venue = venue

            event.facebook_rsvp_url = e_json_obj['facebook_rsvp_url']
            event.ticket_url = e_json_obj['ticket_url']
            event.on_sale_datetime = e_json_obj['on_sale_datetime']
            event.formatted_datetime = e_json_obj['formatted_datetime']
            event.datetime = e_json_obj['datetime']
            event.formatted_location = e_json_obj['formatted_location']
            event.ticket_status = e_json_obj['ticket_status']
            event.BIT_event_id = e_json_obj['id']

            # saving current instance in order to be able to realize many to many relation
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
            return db_event

    def get_media_count(self):
        return Media.objects.filter(event=self.id).count()
