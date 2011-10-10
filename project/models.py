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
Setlist.count = property(lambda s: len(s.song_list))
    
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, primary_key=True)
    phone = models.CharField(verbose_name="phone", max_length=15, blank=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
User.bands = property(lambda u: Band.objects.filter(members__username=u.username))

class Contact(models.Model):
    name = models.CharField(verbose_name="name", max_length=50)
    phone = models.CharField(verbose_name="phone", max_length=15)
    service = models.BooleanField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    added = models.DateField()
    added_by = models.ForeignKey(User)
    
class Band(models.Model):
    name = models.CharField(verbose_name="name", max_length=50)
    bio = models.TextField(verbose_name="bio", max_length=1000, blank=True)
    url = models.URLField(verbose_name="url", blank=True)
    logo = models.ImageField(upload_to="public/bands/") #research this further
    members = models.ManyToManyField(User)
    setlist = models.OneToOneField(Setlist, null=True)
    contacts = models.ManyToManyField(Contact)
    
    def is_member(self, user):
        return len(self.members.filter(username=user.username)) is not 0
        
    def contains_contact(self, contact):
        return len(self.contacts.filter(name=contact.name, phone=contact.phone, service=contact.service, cost=contact.cost)) is not 0

Band.member_list = property(lambda u: u.members.all())
Band.file_list = property(lambda u: u.bandfile_set.all())
Band.calendar_entries = property(lambda u: list(Unavailability.objects.filter(band=u)) + list(Gig.objects.filter(band=u)) + list(Rehearsal.objects.filter(band=u)))
Band.contact_list = property(lambda u: u.contacts.all())

class BandFile(models.Model):
    def get_save_path(instance, filename):
        return '/'.join(['upload_files', str(instance.band.id), filename])

    description = models.CharField(verbose_name="description", max_length=50, blank=True)
    filename = models.CharField(verbose_name="filename", max_length=255)
    size = models.CharField(verbose_name="size", max_length=20)
    uploader = models.CharField(verbose_name="uploader", max_length=50)
    band = models.ForeignKey(Band)
    created = models.DateField()
    file = models.FileField(upload_to=get_save_path)
    attachments = models.ManyToManyField(Song)

class CalendarEntry(models.Model):
    class Meta:
        abstract = True
    date_start = models.DateField()
    time_start = models.CharField(verbose_name="start", max_length=5)
    time_end = models.CharField(verbose_name="end", max_length=5)
    band = models.ForeignKey(Band)
    added_by = models.ForeignKey(User)

class Unavailability(CalendarEntry):
    all_day = models.BooleanField()
    date_end = models.DateField(null=True)

class Rehearsal(CalendarEntry):
    pass # TBD

class Gig(CalendarEntry):
    place = models.CharField(max_length=30)

class EventSetlist(Setlist):
    pass # eventually will hold the event-specific setlist (subset of songs from main setlist)

class UserInvitation(models.Model):
    key = models.CharField(primary_key=True, max_length=100)
    email = models.EmailField(unique=True)
    band = models.ForeignKey(Band, unique=True)
