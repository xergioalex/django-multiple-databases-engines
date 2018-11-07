from bsolutions.users.models import User
from django.db import models
import factory
import factory.django
import factory.fuzzy
# from enumfields import EnumIntegerField

class Cliente(models.Model):
    TIPOS_DOCUMENTOS = (
        (1, 'Cédula de ciudadanía'),
        (2, 'Tarjeta de identidad'),
        (3, 'Pasaporte'),
        (4, 'Cédula de extranjería'),
    )

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False)
    nombre = models.CharField(max_length=45, null=False)
    correo = models.EmailField(max_length=45, null=False)
    documento = models.CharField(max_length=20, null=False)
    tipoDocumento = models.IntegerField(null=False, choices=TIPOS_DOCUMENTOS)
    direccion = models.CharField(max_length=80, null=True)
    telefono = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "cliente"

    def __str__(self):
        return '%s' % (self.nombre)


DOCUMENTOS_IDS = [x[0] for x in Cliente.TIPOS_DOCUMENTOS]


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User

    email = factory.Faker('email')
    name = factory.Faker('name')
    username = factory.Faker('user_name')
    password = factory.Faker('password')

    is_superuser = False
    is_staff = False
    is_active = True


class ClienteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cliente

    user = factory.SubFactory(UserFactory)
    nombre = factory.Faker('name')
    correo = factory.Faker('email')
    documento = factory.Faker('itin')
    tipoDocumento = factory.fuzzy.FuzzyChoice(DOCUMENTOS_IDS)
    direccion = factory.Faker('address')
    telefono = factory.Faker('phone_number')
