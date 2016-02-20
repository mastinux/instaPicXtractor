from django.db import models
from django.utils import timezone
from .bandsintown import Client
from instaPhotoCollector.models import *

client = client = Client('myappid')
# https://github.com/jolbyandfriends/python-bandsintown


class Artist(models.Model):
    facebook_page_url = models.CharField(max_length=511, null=True)
    upcoming_event_count = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    tracker_count = models.IntegerField(default=0)
    mbid = models.CharField(max_length=255, null=True)
    image_url = models.CharField(max_length=511)
    facebook_tour_dates_url = models.CharField(max_length=511, null=True)
    thumb_url = models.CharField(max_length=511)

    def __unicode__(self):
        string = "Artist = %s [image_url:%s, upcoming_events=%s]" % (self.name, self.image_url, self.upcoming_event_count)
        return string

    def is_stored(self):
        if Artist.objects.filter(name=self.name):
            return True
        else:
            return False

    def parse_data(self, a_json_obj):
        self.facebook_page_url = a_json_obj['facebook_page_url']
        self.upcoming_event_count = a_json_obj['upcoming_event_count']
        self.name = a_json_obj['name']
        self.tracker_count = a_json_obj['tracker_count']
        self.mbid = a_json_obj['mbid']
        self.image_url = a_json_obj['image_url']
        self.facebook_tour_dates_url = a_json_obj['facebook_tour_dates_url']
        self.thumb_url = a_json_obj['thumb_url']

    @staticmethod
    def find(artist_name):
        result = client.get(artist_name)
        artist = Artist()
        artist.parse_data(result)
        return artist

    def get_event_by_date(self, search_date):
        results = client.events(self.name, date=search_date)
        event = Event()
        events = list()
        for result in results:
            event.parse_and_save_data(result)
            events.append(event)
        return events

    def get_events_by_dates_range(self, start_date, end_date):
        dates_range = "%s,%s" % (start_date, end_date)
        results = client.events(self.name, date=dates_range)
        events = list()
        for result in results:
            event = Event()
            event.parse_and_save_data(result)
            events.append(event)
        return events

    def get_event_by_location(self, location_name):
        result = client.search(self.name, location=location_name)
        event = Event()
        event.parse_and_save_data(result[0])
        return event

    def get_event_by_location_and_radius(self, location_name, radius):
        # maximum radius value : 241 km (150 miles)
        result = client.search(self.name, location=location_name, radius=radius*0.621371)
        event = Event()
        event.parse_and_save_data(result[0])
        return event

    def get_recommended_events_by_location(self, location):
        results = client.recommended(self.name, location=location, only_recs=True)
        events = list()
        for result in results:
            print " >>> !!! RECOMMENDED EVENT !!!"
            print result
            event = Event.parse_and_save_data(result)
            events.append(event)
        return events

    def get_recommended_events_by_location_and_radius(self, location_name, radius):
        # maximum radius value : 241 km (150 miles)
        results = client.recommended(self.name, location=location_name, radius=radius*0.621371)
        events = list()
        for result in results:
            event = Event()
            event.parse_and_save_data(result)
            events.append(event)
        return events


class Venue(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255, null=True)
    region = models.CharField(max_length=255, null=True)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)

    def __unicode__(self):
        string = "Venue = %s [city:%s, country:%s, latitude:%f, longitude:%f]" % (self.name, self.city, self.country,
                                                                                  self.latitude, self.longitude)
        return string

    def is_stored(self):
        result = Venue.objects.filter(name=self.name, longitude=self.longitude, latitude=self.latitude)
        if result:
            return True
        else:
            return False

    def parse_data(self, v_json_obj):
        #print v_json_obj
        self.city = v_json_obj['city']
        self.name = v_json_obj['name']
        self.country = v_json_obj['country']
        self.region = v_json_obj['region']
        self.longitude = float(v_json_obj['longitude'])
        self.latitude = float(v_json_obj['latitude'])
        #print self


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
        string = "Event = %s [@%s, datetime:%s]" % (self.title, self.venue, self.datetime)

        return string

    def is_stored(self):
        result = Event.objects.filter(BIT_event_id=self.BIT_event_id)
        if result:
            return True
        else:
            return False

    @staticmethod
    def parse_and_save_data(e_json_obj):
        #print e_json_obj
        db_event = Event.objects.filter(BIT_event_id=e_json_obj['id'])
        if not db_event:
            #print 'log >>> saving event on DB'
            event = Event()
            event.description = e_json_obj['description']
            event.title = e_json_obj['title']
            event.ticket_type = e_json_obj['ticket_type']
            # extracting venue
            venue_json_obj = e_json_obj['venue']
            venue = Venue()
            venue.parse_data(venue_json_obj)
            # checking venue
            if not venue.is_stored():
                venue.save()
            else:
                venue = Venue.objects.filter(name=venue.name, longitude=venue.longitude, latitude=venue.latitude).first()
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
            artist = Artist()
            artists = list()

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
            return event
        else:
            """
            for f in Event._meta.get_all_field_names():
                print f
                setattr(self, f, getattr(db_event, f))
            """
            print 'log >>> event already on DB'
            return db_event

    def get_media_count(self):
        return Media.objects.filter(event=self.id).count()
