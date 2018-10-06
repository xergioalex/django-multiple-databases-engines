from django.db import models

class Beacon(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "beacons"

    def __str__(self):
        return '%s' % (self.name)
