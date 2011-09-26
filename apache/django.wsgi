import os
import sys
path = '/home/ubuntu/bandontherun'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_deploy'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
