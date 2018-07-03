from django.db import models


class UploadImage(models.Model):
    image = models.ImageField()

    def __str__(self):
        return self.image.url



# Create your models here.
