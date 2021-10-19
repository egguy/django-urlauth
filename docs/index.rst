.. django-urlauth documentation master file, created by
   sphinx-quickstart on Sat Jan  2 01:45:43 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=======================
django-urlauth overview
=======================

This django application allows you to build special link. When somebody goes via this link to your site he will be automatically authenticated. This is acheaved with special GET arguments which is appended to the link. Such links are usually used in the emails.

Example of such link: http://domain.com/profile/edit/?authkey=SOME_HASH

Simplest example of using django-urlauth::

    >>> from urlauth.models import AuthKey
    >>> AuthKey.objects.wrap_url('http://domain.com/path/', uid=10)
    http://domain.com/path/?authkey=404787ca65ea256e120af7e5e3c217170b1755ad'


Installation and Configuration
==============================

Few easy steps:

* Add ``urlauth`` to ``INSTALLED_APPS``
* Add ``urlauth.middleware.AuthKeyMiddleware`` to ``MIDDLEWARE_CLASSES`` between SessionMiddleware and AuthenticationMiddleware)
* Do syncdb or migrate is you are using south


Extra data
==========

It is possible to store extra data in ``AuthKey`` instance. All arguments of ``wrap_url`` function except ``uid``, ``expired`` and ``onetime`` will be saved in the key instance and will be accessible later via ``extra`` property.

Example of using extra data::

    >>> from urlauth.models import AuthKey
    >>> from urlauth.util import load_key
    >>> url = AuthKey.objects.wrap_url('http://google.com', uid=13, foo='bar', baz=100)
    >>> url
    'http://google.com?authkey=b68b4e38c0356c3eeb7a7ec6849a2dfc86902a10'
    >>> hash = url.split('=')[1]
    >>> key = load_key(hash)
    >>> key.extra
    {u'foo': u'bar', u'baz': 100}


AutKey processing
=================

Main purpose of ``urlauth.middleware.AuthKeyMiddleware`` is to authenticate users. If ``onetime`` property of the AuthKey instance is ``True`` then that key is not deleted from database and also placed in the ``request.authkey`` attribute. Keys with false `onetime`` property are deleted immediatelly after processing.


Signals
=======

.. module:: urlauth.signals


``urlauth.middleware.AuthKeyMiddleware`` generates ``authkey_processed`` signal.  It provides ``key``, ``request`` and ``user`` arguments to his listeners.

.. data:: authkey_processed

    Sent when valid ``AuthKey`` instance is loaded in AuthKeyMiddleware.


Settings
========

django-urlauth have a number of settings. You have to include default settings in your "settings.py" file with the ``from urlauth.settings import *`` command.

``URLAUTH_AUTHKEY_TIMEOUT``

    The number of seconds which generated ``AuthKey`` instance is valid.

``URLAUTH_AUTHKEY_NAME``

    Name of the argument used in the urls to store the hash of generated ``AuthKey`` instance.

Feedback
========

Bitbucket issues page: https://bitbucket.org/lorien/django-urlauth/issues

Email: lorien@lorien.name


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
