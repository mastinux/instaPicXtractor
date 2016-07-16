__author__ = 'mastinux'
from . import views
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index_view'),
    # initial testing
    url(r'^search/$', views.search, name='search_view'),
    url(r'^popular/$', views.popular, name='popular_view'),
    url(r'^location/$', views.search_by_location, name='location_view'),
    # maintenance
    url(r'^init_db/$', views.init_db),
    url(r'^update_artists/$', views.update_artists),
    url(r'^retrieve_all_events_media/$', views.retrieve_all_events_media),
    url(r'^retrieve_artists_events/$', views.retrieve_artists_events),
    # browsing
    url(r'^artists/$', views.get_artists, name='artists_view'),
    url(r'^artist/(?P<artist_name>[\w|\W]+)/(?P<page>[0-9]+)/$', views.explore_artist, name='artist_view'),
    url(r'^event/(?P<event_id>[0-9]+)/(?P<page>[0-9]+)/$', views.explore_event, name='event_view'),
    # IdataCollector testing
    url(r'^test/$', views.test, name='test_view'),
    url(r'^test_authorized/$', views.test_2, name='test_2_view'),

]
