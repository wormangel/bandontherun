from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, primary_key=True)
    
    # User already contains first_name and last_name. remove this?
    name = models.CharField(verbose_name="nome", max_length=50, blank=True)
    phone = models.CharField(verbose_name="telefone", max_length=15, blank=True)

    # one way of doing this (the other would be bidirectional relationship)
    @property
    def bands(self):
        return Band.objects.filter(members__contains=self)

class Band(models.Model):
    name = models.CharField(verbose_name="nome", max_length=50, blank=False)
    bio = models.TextField(verbose_name="bio", max_length=1000, blank=False)
    url = models.URLField(verbose_name="url")
    logo = models.ImageField(upload_to="res/img_bands/") #research this further
    members = models.ManyToManyField(User)

