from django.db import models


class Media(models.Model):
    instagram_id = models.CharField(max_length=256, unique=True)
    std_resolution_url = models.CharField(max_length=512)
    low_resolution_url = models.CharField(max_length=512)
    thumbnail_url = models.CharField(max_length=512)
    location = models.CharField(max_length=1024)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    created_time = models.DateTimeField()
    like_count = models.IntegerField(default=0)
    # todo : change in foreign key to Event in BITdataCollector
    # Field defines a relation with model 'Event', which is either not installed, or is abstract.
    event = models.IntegerField()

    def __unicode__(self):
        string = "media = %s [created_time:%s, latitude:%f, longitude:%f]" % \
                 (self.std_resolution_url, self.created_time, float(self.latitude), float(self.longitude))

        return string
