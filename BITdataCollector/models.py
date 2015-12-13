from django.db import models
import json


class Artist(models.Model):
    facebook_page_url = models.CharField(max_length=511)
    upcoming_event_count = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    tracker_count = models.IntegerField(default=0)
    mbid = models.CharField(max_length=255, null=True)
    image_url = models.CharField(max_length=511)
    facebook_tour_dates_url = models.CharField(max_length=511)
    thumb_url = models.CharField(max_length=511)

    def __unicode__(self):
        string = "%s [image_url:%s, upcoming_events=%s]" % (self.name, self.image_url, self.upcoming_event_count)
        return string

    def parse_data(self, a_json_obj):
        self.facebook_page_url = a_json_obj['facebook_page_url']
        self.upcoming_event_count = a_json_obj['upcoming_event_count']
        self.name = a_json_obj['name']
        self.tracker_count = a_json_obj['tracker_count']
        self.mbid = a_json_obj['mbid']
        self.image_url = a_json_obj['image_url']
        self.facebook_tour_dates_url = a_json_obj['facebook_tour_dates_url']
        self.thumb_url = a_json_obj['thumb_url']


class Venue(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255, null=True)
    region = models.CharField
    longitude = models.FloatField
    latitude = models.FloatField

    def __unicode__(self):
        string = "%s [latitude:%s longitude:%s ]" % (self.name, self.latitude, self.longitude)
        return string

    def parse_data(self, v_json_obj):
        #print v_json_obj
        self.city = v_json_obj['city']
        self.name = v_json_obj['name']
        self.country = v_json_obj['country']
        self.region = v_json_obj['region']
        self.longitude = v_json_obj['longitude']
        self.latitude = v_json_obj['latitude']
        #print self


class Event(models.Model):
    description = models.CharField(max_length=1023)
    title = models.CharField(max_length=511)
    ticket_type = models.CharField(max_length=255)
    venue = models.ForeignKey('Venue')
    facebook_rsvp_url = models.CharField(max_length=511)
    ticket_url = models.CharField(max_length=511)
    on_sale_datetime = models.DateTimeField
    formatted_datetime = models.CharField(max_length=255)
    datetime = models.DateTimeField
    formatted_location = models.CharField(max_length=255)
    artists = models.ManyToManyField(Artist)
    ticket_status = models.CharField(max_length=255)
    event_id = models.IntegerField

    def parse_data(self, e_json_obj):
        self.description = e_json_obj['description']
        self.title = e_json_obj['title']
        self.ticket_type = e_json_obj['ticket_type']

        #checking venue
        venue_json_obj = e_json_obj['venue']
        venue = Venue()
        venue.parse_data(venue_json_obj)
        #TODO: improve DB check method
        #TODO: problems checking latitude and longitude
        results = Venue.objects.filter(name=venue.name, city=venue.city)
        self.venue = results[0]

        #TODO: continue developing
        self.facebook_rsvp_url = e_json_obj['facebook_rsvp_url']
        self.ticket_url = e_json_obj['ticket_url']
        self.on_sale_datetime = e_json_obj['on_sale_datetime']
        self.formatted_datetime = e_json_obj['formatted_datetime']
        self.datetime = e_json_obj['datetime']
        self.formatted_location = e_json_obj['formatted_location']
        #TODO : check artists
        self.artists = e_json_obj['artists']
        self.ticket_status = e_json_obj['ticket_status']
        self.event_id = e_json_obj['id']

    def __unicode__(self):
        string = "%s [venue:%s, datetime:%s]" % (self.title, self.venue, self.datetime)
        return string
