import hashlib

from django.contrib.auth.models import User
from models import Band
from models import UserInvitation

from celery.task import Task
from celery.registry import tasks

import users_manager

class UserInvitationTask(Task):

    def run(self, email, inviter, band, **kwargs):
        try:
            key = hashlib.sha224(email).hexdigest()
            if not users_manager.invitation_exists(key):
                invitation = users_manager.create_invitation(email, key, band)
                invitation.save()
            else:
                invitation = users_manager.get_invitation(key)
            
            link = "http://localhost:8000/create/user/%s" % invitation.key
            body = "You were invited by %s to be part of %s on Band on the Run plataform. \
                    Please visit the follow link to create your profile. %\
                    <a href=\"%s\">%s</a>" % inviter.first_name band.name link link
            print body
            #send_mail('Invite to Band on the Run', body, 'admin@bandontherun.com', [email], fail_silently=False)
        except Exception, e:
            print e

tasks.register(NewUserTask)
