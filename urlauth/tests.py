import cgi
from datetime import datetime, timedelta

from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase

from urlauth.models import AuthKey
from urlauth.settings import URLAUTH_AUTHKEY_NAME
from urlauth.signals import authkey_processed
from urlauth.util import InvalidKey, load_key

User = get_user_model()


class UrlauthTestCase(TestCase):
    urls = "urlauth.tests"
    test_url = "/urlauth_test_view/"

    # Helpers
    def setUp(self):
        """
        Create active and inactive users.
        """

        User.objects.all().delete()
        self.user = User.objects.create_user("user", "user@host.com", "pass")
        self.ban_user = User.objects.create_user(
            "ban_user", "ban_user@host.com", "pass"
        )
        self.ban_user.is_active = False
        self.ban_user.save()

    def process_url(self, url, **kwargs):
        """
        Add authkey to the ``url`` and then open that url with django test client.

        Returns:
            The ID of created ``AuthKey`` instance
        """

        url = AuthKey.objects.wrap_url(url, **kwargs)
        path, args = url.split("?")[0], cgi.parse_qs(url.split("?")[1])
        self.client.get(url, args)
        return args[URLAUTH_AUTHKEY_NAME][0]

    # Test cases

    def test_create_key(self):
        "Test the create_key function"
        self.assertTrue(
            AuthKey.objects.create_key(uid=self.user.pk, expired=datetime.now())
        )

    def test_wrap_url(self):
        "Test the wrap_url function"
        expired = datetime.now()

        AuthKey.objects.all().delete()
        clean_url = "http://ya.ru"
        url = AuthKey.objects.wrap_url(clean_url, uid=self.user.pk, expired=expired)
        key = AuthKey.objects.get()
        self.assertEqual(
            url, "{}?{}={}".format(clean_url, URLAUTH_AUTHKEY_NAME, key.id)
        )

        AuthKey.objects.all().delete()
        clean_url = "http://ya.ru?foo=bar"
        url = AuthKey.objects.wrap_url(clean_url, uid=self.user.pk, expired=expired)
        key = AuthKey.objects.get()
        self.assertEqual(
            url, "{}&{}={}".format(clean_url, URLAUTH_AUTHKEY_NAME, key.id)
        )

        # Test url with hash
        AuthKey.objects.all().delete()
        clean_url = "http://ya.ru#hash"
        url = AuthKey.objects.wrap_url(clean_url, uid=self.user.pk, expired=expired)
        key = AuthKey.objects.get()
        self.assertEqual(
            url, "http://ya.ru?{}={}#hash".format(URLAUTH_AUTHKEY_NAME, key.id)
        )

        # Test url with hash and non-empty querystring
        AuthKey.objects.all().delete()
        clean_url = "http://ya.ru?foo=bar#hash"
        url = AuthKey.objects.wrap_url(clean_url, uid=self.user.pk, expired=expired)
        key = AuthKey.objects.get()
        self.assertEqual(
            url, "http://ya.ru?foo=bar&{}={}#hash".format(URLAUTH_AUTHKEY_NAME, key.id)
        )

    def test_validate_key(self):
        "Test the validate_key function"
        expired = datetime.now() - timedelta(seconds=1)
        key = AuthKey.objects.create_key(uid=self.user.pk, expired=expired, foo="bar")
        self.assertRaises(InvalidKey, lambda: load_key(key))

        expired = datetime.now() + timedelta(seconds=10)
        key = AuthKey.objects.create_key(uid=self.user.pk, expired=expired)
        self.assertTrue(load_key(key))

    def test_authentication(self):
        "Test the authentication middleware"
        expired = datetime.now() + timedelta(days=1)
        resp = self.client.get(self.test_url)

        # Guest is not authenticated
        self.client.logout()
        self.assertFalse("_auth_user_id" in self.client.session)

        ## Simple authorization
        self.client.logout()
        self.process_url(self.test_url, uid=self.user.pk, expired=expired)
        # self.assertEqual(self.client.session, self.user.pk)

        self.assertEqual(self.client.session["_auth_user_id"], str(self.user.pk))

        ## Baned user can't authorize
        self.client.logout()
        self.process_url(self.test_url, uid=self.ban_user.pk, expired=expired)
        self.assertFalse("_auth_user_id" in self.client.session)

        ## Expired auth key does not work
        self.client.logout()
        expired = datetime.now() - timedelta(seconds=1)
        self.process_url(self.test_url, uid=self.user.pk, expired=expired)
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_signals(self):
        logs = []

        def handler(**k):
            return logs.append("X")

        authkey_processed.connect(handler)

        self.assertEqual(0, len(logs))
        self.client.logout()
        expired = datetime.now() + timedelta(days=1)
        self.process_url(self.test_url, uid=self.user.pk, expired=expired)
        self.assertEqual(1, len(logs))

    def test_onetime_feature(self):
        self.client.logout()
        expired = datetime.now() + timedelta(days=1)
        hash = self.process_url(self.test_url, uid=self.user.pk, expired=expired)
        self.assertFalse(AuthKey.objects.filter(id=hash).count())

        self.client.logout()
        expired = datetime.now() + timedelta(days=1)
        hash = self.process_url(
            self.test_url, uid=self.user.pk, expired=expired, onetime=False
        )
        self.assertTrue(AuthKey.objects.filter(id=hash).count())

    def test_bulk(self):
        User.objects.all().delete()
        AuthKey.objects.all().delete()
        for x in range(100):
            username = "test%d" % x
            User.objects.create_user(username, "%s@gmail.com" % username, username)
        users = User.objects.all()
        for user in users:
            obj = AuthKey.objects.wrap_url("/", uid=user.pk)
        self.assertEqual(User.objects.count(), AuthKey.objects.count())


def test_view(request):
    return HttpResponse("")


urlpatterns = [
    url("urlauth_test_view/", test_view, name="urlauth_test_view"),
]
