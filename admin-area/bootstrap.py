#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_area.settings')
django.setup()

from django.core import management  # noqa
from django.contrib.auth.models import User  # noqa


# migrate
management.call_command('migrate', interactive=False)

# create admin, if needed
admin_user = os.environ.get('ADMIN_USER', 'admin')

if not User.objects.filter(username=admin_user).exists():
    admin_email = os.environ.get('ADMIN_EMAIL')
    if not admin_email:
        print('ADMIN_EMAIL environment variable is not set.')
        sys.exit(1)
    admin_password = os.environ.get('ADMIN_PASSWORD')
    if not admin_password:
        print('ADMIN_PASSWORD environment variable is not set.')
        sys.exit(1)
    User.objects.create_superuser(admin_user, admin_email, admin_password)
