from django.db import models

class Notifications(models.Model):
    # notifications
    # idProduct
    # idBeacon
    # name = models.CharField(max_length=45)
    # reference = models.CharField(max_length=45)
    # price = models.FloatField()
    # idProductType

    class Meta:
        verbose_name_plural = "notifications"

    def __str__(self):
        return '%s' % (self.name)
