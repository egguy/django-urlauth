from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin

from urlauth.models import AuthKey
from urlauth.settings import URLAUTH_AUTHKEY_NAME
from urlauth.signals import authkey_processed
from urlauth.util import InvalidKey, load_key

User = get_user_model()


class AuthKeyMiddleware(MiddlewareMixin):
    """
    This middleware can authenticate user with an auth key in HTTP request.
    """

    def process_request(self, request):
        key = request.GET.get(
            getattr(settings, "URLAUTH_AUTHKEY_NAME", URLAUTH_AUTHKEY_NAME)
        )
        user = None
        if key is None:
            return
        try:
            key = load_key(key)
            if key.uid:
                try:
                    user = User.objects.get(pk=key.uid)
                except User.DoesNotExist:
                    raise InvalidKey("User [pk=%s] does not exist" % user.pk) from None
        except InvalidKey:
            return

        authkey_processed.send(sender=AuthKey, key=key, request=request, user=user)

        if user and user.is_active:
            user.backend = "django.contrib.auth.backends.ModelBackend"
            auth.login(request, user)

        if key.onetime:
            key.delete()

        request.authkey = key
