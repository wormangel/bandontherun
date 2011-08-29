# TODO: separate in two apps (user, band)
from django.db import models
from django.contrib.auth.models import User

# entities
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, primary_key=True)
    phone = models.CharField(verbose_name="phone", max_length=15, blank=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
User.bands = property(lambda u: Band.objects.filter(members__username=u.username))

class Band(models.Model):
    name = models.CharField(verbose_name="name", max_length=50, blank=False)
    shortcut_name = models.CharField(verbose_name="shortcut name", max_length=50, blank=False, unique=True)
    bio = models.TextField(verbose_name="bio", max_length=1000, blank=False)
    url = models.URLField(verbose_name="url")
    logo = models.ImageField(upload_to="static/bands/") #research this further
    members = models.ManyToManyField(User)

    def is_member(user):
        return len(Band.objects.filter(members__user=user)) is not 0

Band.member_list = property(lambda u: u.members.all())
