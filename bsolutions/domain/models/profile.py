from django.db import models
from django.contrib.postgres.fields import JSONField

# from enumfields import EnumIntegerField


class Profile(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    document_number = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    direction = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    # photo = models.ImageField(upload_to=profile_photo_path,
    #                           null=True,
    #                           blank=True)
    # phone = models.CharField(max_length=20)
    # phone_code = models.CharField(max_length=4)
    # lang = models.CharField(max_length=2)
    # gdpr = JSONField()
    # answers = JSONField()

    def __str__(self):
        return '%s %s' % (self.name, self.lastname)
