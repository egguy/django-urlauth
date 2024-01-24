import logging
from datetime import datetime

from urlauth.models import AuthKey


class InvalidKey(Exception):
    pass


def wrap_url(url, **kwargs):
    """
    Create a new authorization key and append it to the url.
    """

    logging.error(
        "urlauth.util.wrap_url is deprecated. Use AuthKey.objects.wrap_url instead."
    )
    return AuthKey.objects.wrap_url(url, **kwargs)


def load_key(hash):
    """
    Load key record associated with given hash.
    """

    try:
        key = AuthKey.objects.get(pk=hash)
    except AuthKey.DoesNotExist:
        raise InvalidKey("Key does not exist")
    if datetime.now() > key.expired:
        raise InvalidKey("Key is expired")
    return key
