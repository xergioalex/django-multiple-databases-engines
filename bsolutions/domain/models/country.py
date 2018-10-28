from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2)
    phone_code = models.CharField(max_length=4)

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self):
        return '%s' % (self.name)
