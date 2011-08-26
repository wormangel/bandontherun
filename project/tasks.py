from celery.task import Task
from celery.registry import tasks
from models import Band
from django.contrib.auth.models import User

import bands_manager

class NewUserTask(Task):

    def run(self, shortcut_name, user_email, **kwargs):
        try:
            # create user
            # save user
            # send mail
            band = bands_manager.get_band(shortcut_name)
            # add as member of the band
        except Exception, e:
            print e

tasks.register(NewUserTask)
