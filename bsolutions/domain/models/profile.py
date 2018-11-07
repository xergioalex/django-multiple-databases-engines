from django.db import models

# from enumfields import EnumIntegerField


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=45, null=False)
    correo = models.EmailField(max_length=45, null=False)
    documento = models.CharField(max_length=20, null=False)
    tipoDocumento = models.IntegerField(null=False)
    direccion = models.CharField(max_length=80, null=True)
    telefono = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "cliente"

    def __str__(self):
        return '%s' % (self.nombre)
