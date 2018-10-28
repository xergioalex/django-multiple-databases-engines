from django.db import models

class Product(models.Model):
    # idClient
    # idProduct
    # cant
    # discount
    # paymentData
    # name = models.CharField(max_length=45)
    # reference = models.CharField(max_length=45)
    # price = models.FloatField()
    # idProductType

    class Meta:
        verbose_name_plural = "products"

    def __str__(self):
        return '%s' % (self.name)
