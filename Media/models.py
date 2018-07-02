from django.db import models
from django.forms.models import modelform_factory


class UploadImage(models.Model):
    image = models.ImageField()

    def __str__(self):
        return self.image.url

    def num(self):
        return self.objects.all().count()

UploadImageForm = modelform_factory(UploadImage, fields= ('image',))

# Create your models here.
