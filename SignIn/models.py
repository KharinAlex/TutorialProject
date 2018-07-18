from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserModel(models.Model):
    user_id = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    about = models.TextField(default="")
    birthday = models.DateField(default="1970-01-01")
    country = models.CharField(max_length=15, default="")
    photo = models.ImageField(default="default_photo.png")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserModel.objects.create(user_id=instance)

# Create your models here.
