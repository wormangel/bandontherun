import hashlib, settings

from celery.task import Task
from celery.registry import tasks

import users_manager

class UserInvitationTask(Task):

    def run(self, email, inviter, band, **kwargs):
        try:
            key = hashlib.sha224(email).hexdigest()
            print key
            if users_manager.invitation_exists(key):
                invitation = users_manager.get_invitation(key)
            else:
                invitation = users_manager.create_invitation(email, key, band)
                invitation.save()
            link = "http://localhost:8000/user/create/%s" % invitation.key
            body = "You were invited by %s to be part of %s on Band on the Run plataform. \
                    Please visit the follow link to create your profile. \
                    <a href=\"%s\">%s</a>" % (inviter.get_full_name(), band.name, link, link)
            #send_mail('Invite to Band on the Run', body, 'admin@bandontherun.com', [email], fail_silently=False)
        except Exception, e:
            print e

tasks.register(UserInvitationTask)
