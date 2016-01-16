__author__ = 'mastinux'
from . import views
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index_view'),
    url(r'^search', views.search, name='search_view'),
    url(r'^popular', views.popular, name='popular_view'),
    url(r'^location', views.search_by_location, name='location_view'),
]