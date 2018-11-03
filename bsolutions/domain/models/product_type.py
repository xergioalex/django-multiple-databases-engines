from django.db import models

class TipoProducto(models.Model):
    nombre = models.CharField(max_length=45)
    # idProductType

    class Meta:
        verbose_name_plural = "product_types"

    def __str__(self):
        return '%s' % self.nombre
