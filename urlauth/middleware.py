from builtins import object
from django.contrib import auth
from django.conf import settings
from urlauth.settings import URLAUTH_AUTHKEY_NAME

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from urlauth.util import load_key, InvalidKey
from urlauth.models import AuthKey
from urlauth.signals import authkey_processed


class AuthKeyMiddleware(object):
    """
    This middleware can authenticate user with auth key in HTTP request.
    """

    def process_request(self, request):
        key = request.REQUEST.get(getattr(settings, "URLAUTH_AUTHKEY_NAME", URLAUTH_AUTHKEY_NAME))
        user = None
        if key is None:
            return
        try:
            key = load_key(key)
            if key.uid:
                try:
                    user = User.objects.get(pk=key.uid)
                except User.DoesNotExist:
                    raise InvalidKey('User [pk=%s] does not exist' % user.pk)
        except InvalidKey:
            return

        authkey_processed.send(sender=AuthKey, key=key, request=request, user=user)

        if user and user.is_active:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)    

        if key.onetime:
            key.delete()

        request.authkey = key
