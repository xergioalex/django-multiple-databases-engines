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

    GENEROS = (
        ('F', 'Femenino'),
        ('M', 'Masculino'),
    )

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False)
    nombre = models.CharField(max_length=45, null=False)
    correo = models.EmailField(max_length=45, null=False)
    documento = models.CharField(max_length=20, null=False)
    tipoDocumento = models.IntegerField(choices=TIPOS_DOCUMENTOS, null=False)
    genero = models.CharField(max_length=1, choices=GENEROS, null=True)
    edad = models.PositiveIntegerField(null=False)
    direccion = models.CharField(max_length=80, null=True)
    telefono = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "cliente"

    def __str__(self):
        return '%s' % (self.nombre)


DOCUMENTOS_IDS = [x[0] for x in Cliente.TIPOS_DOCUMENTOS]
GENEROS_IDS = [x[0] for x in Cliente.GENEROS]


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)
        exclude = ('username_sequence', 'username_generated')

    # Excluded
    username_sequence = factory.Sequence(lambda n: "user_%d" % n)
    username_generated = factory.Faker('user_name')

    email = factory.Faker('email')
    name = factory.Faker('name')
    username = factory.LazyAttribute(lambda p: '{} {}'.format(p.username_sequence, p.username_generated))
    password = factory.Faker('password')

    is_superuser = False
    is_staff = False
    is_active = True


class ClienteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cliente
        django_get_or_create = ('id',)

    id = factory.fuzzy.FuzzyInteger(0, 100000)
    user = factory.SubFactory(UserFactory)
    nombre = factory.Faker('name')
    correo = factory.Faker('email')
    documento = factory.Faker('itin')
    tipoDocumento = factory.fuzzy.FuzzyChoice(DOCUMENTOS_IDS)
    genero = factory.fuzzy.FuzzyChoice(GENEROS_IDS)
    edad = factory.fuzzy.FuzzyInteger(1, 100)
    direccion = factory.Faker('address')
    telefono = factory.Faker('phone_number')
