from django.db import models
from django.contrib.auth.models import User

class Song(models.Model):
    artist = models.CharField(verbose_name="artist", max_length=50)
    title = models.CharField(verbose_name="title", max_length=80)

class Setlist(models.Model):
    name = models.CharField(verbose_name="name", max_length=50)
    songs = models.ManyToManyField(Song)

    def contains(self, song):
        return len(self.songs.filter(artist=song.artist, title=song.title)) is not 0

Setlist.song_list = property(lambda s: s.songs.all())

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
    setlist = models.ForeignKey(Setlist, null=True, unique=True)

    def is_member(self, user):
        return len(self.members.filter(username=user.username)) is not 0

Band.member_list = property(lambda u: u.members.all())
Band.file_list = property(lambda u: u.bandfile_set.all())
Band.set_list = property(lambda b: Setlist.objects.get_or_create(pk=b.id)[0])

class BandFile(models.Model):
    def get_save_path(instance, filename):
        return '/'.join(['upload_files', str(instance.band.id), filename])

    name = models.CharField(verbose_name="name", max_length=50)
    filename = models.CharField(verbose_name="filename", max_length=255)
    size = models.CharField(verbose_name="size", max_length=20)
    uploader = models.CharField(verbose_name="uploader", max_length=50)
    band = models.ForeignKey(Band)
    created = models.DateField()
    file = models.FileField(upload_to=get_save_path)
    attachments = models.ManyToManyField(Song)

class EventSetlist(Setlist):
    pass # eventually will hold the event-specific setlist (subset of songs from main setlist)

class UserInvitation(models.Model):
    key = models.CharField(primary_key=True, max_length=100)
    email = models.EmailField(unique=True)
    band = models.ForeignKey(Band, unique=True)
