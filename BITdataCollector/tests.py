from django.test import TestCase
from .bandsintown import Client
from .models import *
from django.utils.timezone import timedelta

client = Client('myappid')
artists_names = ['Usher', 'Cage the Elephant', 'Knife Party', 'Steve Aoki', 'Lady Gaga', 'The Weeknd']


class ArtistTestCase(TestCase):
    def setUp(self):
        for artist_name in artists_names:
            result = client.get(artist_name)
            artist = Artist()
            artist.parse_data(result)
            if not artist.is_stored():
                artist.save()

    def test_date_events_search(self):
        artist = Artist.objects.filter(name='The Weeknd').first()
        start = timezone.now() - timedelta(days=12)
        end = timezone.now()

        #TEST : search artist event by date [OK]
        print artist.get_event_by_date(start.date())

        #TEST : search artist events by dates range [OK]
        for e in artist.get_events_by_dates_range(start.date(), end.date()):
            print e

    def test_location_events_search(self):
        #TEST: search artist event by location [OK]
        artist = Artist.find('Madman')
        print artist.get_event_by_location('Turin,IT')

        #TEST: search artist event by location and radius[OK]
        artist = Artist.find('Madman')
        print artist.get_event_by_location_and_radius('Turin,IT', 240)

    def test_location_events_search(self):
        #TEST: search recommended events by location [OK]
        artist = Artist.find('Madman')
        for e in artist.get_recommended_events_by_location('Turin,IT'):
            print e

        #TEST: search recommended events by location and radius [OK]
        artist = Artist.find('Madman')
        for e in artist.get_recommended_events_by_location_and_radius('Turin,IT', 240):
            print e


class EventTestCase(TestCase):
    def setUp(self):
        for artist in Artist.objects.all():
            results = client.events(artist.name)
            for result in results:
                event = Event()
                event.parse_and_save_data(result)