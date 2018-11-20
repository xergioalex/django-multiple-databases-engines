import mongoengine


class EmbeddedUserSocialContext(mongoengine.EmbeddedDocument):
    id = mongoengine.IntField(null=False)
    address = mongoengine.StringField()
    age_range = mongoengine.StringField()
    birthday = mongoengine.StringField()
    context = mongoengine.StringField()
    cover = mongoengine.StringField()
    profile_pic = mongoengine.StringField()
    email = mongoengine.EmailField()
    employee_number = mongoengine.StringField()
    gender = mongoengine.StringField()
    hometown = mongoengine.StringField()
    languages = mongoengine.ListField(field=mongoengine.StringField())
    location = mongoengine.StringField()
    religion = mongoengine.StringField()
    sports = mongoengine.ListField(field=mongoengine.StringField())


class SocialUserMediaDocument(mongoengine.Document):
    userId = mongoengine.IntField(null=False)
    socialContext = mongoengine.EmbeddedDocumentField(EmbeddedUserSocialContext, default=EmbeddedUserSocialContext())

