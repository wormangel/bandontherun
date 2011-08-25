#!/usr/bin/env python
import os
import sys

PROJECT_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.pardir))

sys.path.insert(0, PROJECT_PATH)
sys.path.insert(0, os.path.join(PROJECT_PATH, 'src'))

from django.core.management import execute_manager
try:
    import settings
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
