from django.db import models
from django.contrib.postgres.fields import JSONField

# from enumfields import EnumIntegerField


class Cliente(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    correo = models.EmailField(max_length=45)
    documento = models.CharField(max_length=45, null=True)
    tipoDocumento = models.IntegerField()
    nombre = models.CharField(max_length=45)
    direccion = models.CharField(max_length=80)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return '%s' % (self.nombre)
