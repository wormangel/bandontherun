from django.db import models
from django.contrib.auth.models import User

class Band(models.Model):
    name = models.CharField(verbose_name="name", max_length=50, blank=False)
    bio = models.TextField(verbose_name="bio", max_length=1000, blank=False)
    url = models.URLField(verbose_name="url")
    logo = models.ImageField(upload_to="public/bands/") #research this further
    members = models.ManyToManyField(User)

    def is_member(self, user):
        return len(Band.objects.filter(members__username=user.username)) is not 0

Band.member_list = property(lambda u: u.members.all())
