__author__ = 'mastinux'
from . import views
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index_view'),
    url(r'^search', views.search, name='search_view'),
    url(r'^popular', views.popular, name='popular_view'),
    url(r'^location', views.search_by_location, name='location_view'),
    url(r'^retrieve_artists', views.retrieve_artists, name='artists_view'),
    url(r'^retrieve_all_events_media', views.retrieve_all_events_media),
    url(r'^retrieve_all_artists_events', views.retrieve_all_artists_events),
    url(r'^artist/(?P<artist_name>[\w|\W]+)/(?P<page>[0-9]+)/$', views.explore_artist, name='artist_view'),
    url(r'^event/(?P<event_id>[0-9]+)/(?P<page>[0-9]+)/$', views.explore_event, name='event_view'),
]