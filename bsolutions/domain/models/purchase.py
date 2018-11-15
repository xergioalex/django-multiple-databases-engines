from django.db import models

import factory
import factory.django
import factory.fuzzy

from .product import ProductoFactory
from .profile import ClienteFactory


class Compra(models.Model):
    MEDIO_PAGO = (
        (1, 'Efectivo'),
        (2, 'Tarjeta de debito'),
        (3, 'Tarjeta de credito'),
    )
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey('Cliente', db_column='idCliente', on_delete=models.CASCADE, null=False)
    fecha = models.DateTimeField(auto_now_add=True, null=False)
    medioPago = models.IntegerField(null=False, choices=MEDIO_PAGO)
    descuento = models.FloatField(default=0.0, null=True)

    class Meta:
        db_table = "compra"
        verbose_name_plural = "products"

    def __str__(self):
        return '%s' % (self.cliente_id)


class CompraProducto(models.Model):
    id = models.AutoField(primary_key=True)
    compra = models.ForeignKey('Compra', db_column='idCompra', on_delete=models.CASCADE, null=False)
    producto = models.ForeignKey('Producto', db_column='idProducto', on_delete=models.CASCADE, null=False)
    cantidad = models.PositiveIntegerField(default=1, null=False)
    descuento = models.FloatField(default=0.0, null=True)

    class Meta:
        db_table = "compra_producto"
        verbose_name_plural = "products"

    def __str__(self):
        return '%s' % (self.cantidad)


TIPO_PAGO_IDS = [x[0] for x in Compra.MEDIO_PAGO]


class CompraFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Compra

    cliente = factory.SubFactory(ClienteFactory)
    fecha = factory.Faker('date_time_this_year')
    medioPago = factory.fuzzy.FuzzyChoice(TIPO_PAGO_IDS)
    descuento = factory.fuzzy.FuzzyFloat(0, 100, precision=2)


class CompraProductoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CompraProducto

    compra = factory.SubFactory(CompraFactory)
    producto = factory.SubFactory(ProductoFactory)
    cantidad = factory.fuzzy.FuzzyInteger(1, 200)
    descuento = factory.fuzzy.FuzzyFloat(0, 100, precision=2)
