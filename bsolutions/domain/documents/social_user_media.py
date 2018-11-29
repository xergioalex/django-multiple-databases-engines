import mongoengine
import factory.mongoengine
import factory.fuzzy

from bsolutions.domain.models.beacon import getCoordinate
from bsolutions.domain.models.profile import GENEROS_IDS


class EmbeddedUserSocialContext(mongoengine.EmbeddedDocument):
    id = mongoengine.IntField(null=False)
    address = mongoengine.StringField()
    age_range = mongoengine.StringField()
    birthday = mongoengine.DateField()
    context = mongoengine.StringField()
    cover = mongoengine.StringField()
    profile_pic = mongoengine.StringField()
    email = mongoengine.EmailField()
    employee_number = mongoengine.IntField()
    gender = mongoengine.StringField()
    hometown = mongoengine.StringField()
    languages = mongoengine.ListField(field=mongoengine.StringField())
    location = mongoengine.StringField()
    religion = mongoengine.StringField()
    sports = mongoengine.ListField(field=mongoengine.StringField())


class SocialUserMediaDocument(mongoengine.Document):
    userId = mongoengine.IntField(null=False)
    socialContext = mongoengine.EmbeddedDocumentField(EmbeddedUserSocialContext, default=EmbeddedUserSocialContext())


class EmbeddedUserSocialContextFactory(factory.mongoengine.MongoEngineFactory):

    class Meta:
        model = EmbeddedUserSocialContext

    id = factory.fuzzy.FuzzyInteger(1, 1000000)
    address = factory.Faker('address')
    age_range = factory.Faker('year')
    birthday = factory.Faker('date_of_birth')
    context = factory.Faker('text')
    cover = factory.Faker('file_path')
    profile_pic = factory.Faker('file_path')
    email = factory.Faker('email')
    employee_number = factory.fuzzy.FuzzyInteger(1, 100000)
    gender = factory.fuzzy.FuzzyChoice(GENEROS_IDS)
    hometown = factory.Faker('city')
    languages = factory.Faker('sentences')
    location = factory.LazyAttribute(lambda n: getCoordinate())
    religion = factory.Faker('name')
    sports = factory.Faker('sentences')


class SocialUserMediaDocumentFactory(factory.mongoengine.MongoEngineFactory):

    class Meta:
        model = SocialUserMediaDocument

    userId = factory.fuzzy.FuzzyInteger(1, 100000)
    socialContext = factory.SubFactory(EmbeddedUserSocialContextFactory)

