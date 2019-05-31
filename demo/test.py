#!/usr/bin/env python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.core.management import call_command
from django.conf import settings
from django.contrib.auth import get_user_model


from urlauth.models import AuthKey


User = get_user_model()


def reproduce():
    try:
        os.unlink(settings.DATABASES['default']['NAME'])
    except OSError:
        pass
    call_command('syncdb', interactive=False)
    call_command('flush', interactive=False)

    print 'Creating users'
    for x in xrange(100):
        username = 'test%d' % x
        User.objects.create_user(username, '%s@gmail.com' % username, username)

    users = User.objects.all()

    print 'Creating auth keys'
    for user in users:
        obj = AuthKey.objects.wrap_url('/', uid=user.pk)

    print 'Key count: %d' % AuthKey.objects.count()


if __name__ == '__main__':
    reproduce()
