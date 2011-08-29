from django.db import models
from django.contrib.auth.models import User
from band.models import Band

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, primary_key=True)
    phone = models.CharField(verbose_name="phone", max_length=15, blank=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
User.bands = property(lambda u: Band.objects.filter(members__username=u.username))


