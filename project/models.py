from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, primary_key=True)
    phone = models.CharField(verbose_name="phone", max_length=15, blank=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
User.bands = property(lambda u: Band.objects.filter(members__username=u.username))

class Band(models.Model):
    name = models.CharField(verbose_name="name", max_length=50)
    bio = models.TextField(verbose_name="bio", max_length=1000, blank=True)
    url = models.URLField(verbose_name="url", blank=True)
    logo = models.ImageField(upload_to="public/bands/") #research this further
    members = models.ManyToManyField(User)

    def is_member(self, user):
        return len(Band.objects.filter(members__username=user.username)) is not 0

Band.member_list = property(lambda u: u.members.all())
Band.file_list = property(lambda u: u.bandfile_set.all())

class BandFile(models.Model):
    name = models.CharField(verbose_name="name", max_length=50)
    filename = models.CharField(verbose_name="filename", max_length=255)
    size = models.CharField(verbose_name="size", max_length=20)
    uploader = models.CharField(verbose_name="uploader", max_length=50)
    band = models.ForeignKey(Band)
    created = models.DateField()
    file = models.FileField(upload_to='project/upload_files/')

#class UserInvitation(models.Model):
    #band = models.ForeignKey(Band, unique=True, primary_key=True)
    #email = models.EmailField(primary_key=True, verbose_name="email")
    #key = models.CharField()
