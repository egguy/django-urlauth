import json
from datetime import datetime, timedelta
from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.utils import IntegrityError

from urlauth.settings import URLAUTH_AUTHKEY_NAME, URLAUTH_AUTHKEY_TIMEOUT


class URLAuthError(Exception):
    pass


class AuthKeyManager(models.Manager):
    def create_key(self, uid, expired=None, onetime=True, **kwargs):
        """
        Create AuthKey object and return its ID.
        :param uid: The uid of the user to automatically log
        :param expired: (default:  datetime.now() + timedelta(seconds=settings.URLAUTH_AUTHKEY_TIMEOUT)) datetime.now() + time delta to specify when the key must expire
        :param ontime: (default: True) Generate a one time key
        :param kwargs: others arguments
        :return: An unique auth key
        """

        key = AuthKey()
        key.uid = uid
        if expired:
            key.expired = expired
        else:
            key.expired = datetime.now() + timedelta(
                seconds=getattr(
                    settings, "URLAUTH_AUTHKEY_TIMEOUT", URLAUTH_AUTHKEY_TIMEOUT
                )
            )

        key.onetime = onetime
        key.data = json.dumps(kwargs)

        # Try 10 times to create AuthKey instance with unique PK
        for _ in range(10):
            key.pk = uuid4()  # Use a unique identifier
            try:
                key.save(force_insert=True)
            except IntegrityError:
                key.pk = None
            else:
                break

        if not key.pk:
            raise URLAuthError("Could not create unique key")

        return key.id

    def wrap_url(self, url, uid, **kwargs):
        """
        Create new authorization key, append it to the url and return modified url.
        :param url: The url to wrap
        :param uid: id of the user to log
        :param kwargs: others params used byt create_key
        :return: An url wrapped with an unique key
        """

        key_id = self.create_key(uid, **kwargs)
        clue = "?" in url and "&" or "?"
        parts = url.rsplit("#", 1)
        if len(parts) > 1:
            url, hash = parts
            hash = "#%s" % hash
        else:
            hash = ""
        url = "{}{}{}={}{}".format(
            url,
            clue,
            getattr(settings, "URLAUTH_AUTHKEY_NAME", URLAUTH_AUTHKEY_NAME),
            key_id,
            hash,
        )
        return url


class AuthKey(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    uid = models.PositiveIntegerField(null=True)
    expired = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    onetime = models.BooleanField(blank=True, default=True)
    data = models.TextField()

    objects = AuthKeyManager()

    def __str__(self):
        return "AuthKey #%s" % self.id

    @property
    def extra(self):
        return json.loads(self.data)

    def get_user(self):
        if self.uid:
            return get_user_model().objects.get(pk=self.uid)
        else:
            return None
