from django.db import models


class Postcode(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    code = models.CharField(max_length=200)

    def __str__(self):
        return "({}, {}) -> {}".format(self.lat, self.lon, self.code)
