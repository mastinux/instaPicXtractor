from django.shortcuts import render
from django.http import HttpResponse

#todo : understand how to import already installed app from following URL
# https://github.com/Instagram/python-instagram


def index(request):
    return HttpResponse("Hi, you are in instaPhotoCollector.")
