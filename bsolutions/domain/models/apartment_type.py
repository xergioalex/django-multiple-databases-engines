from django.contrib.gis.db import models
from enumfields import EnumIntegerField
from .enum import ApartmentKind


class ApartmentType(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    kind = EnumIntegerField(ApartmentKind)

    def __str__(self):
        return '%s' % ('ENTIRE' if self.kind == ApartmentKind.ENTIRE else 'SHARED')
