from django.db import models


class Media(models.Model):
    instagram_id = models.IntegerField()
    std_resolution_url = models.CharField(max_length=512)
    low_resolution_url = models.CharField(max_length=512)
    thumbnail_url = models.CharField(max_length=512)