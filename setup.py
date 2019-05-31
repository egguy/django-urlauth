#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = 'django-urlauth',
    version = '0.1.8',
    description = 'Django application for user authentication with key in hypertext link',
    url = 'http://bitbucket.org/lorien/django-urlauth/',
    author = 'Grigoriy Petukhov',
    author_email = 'lorien@lorien.name',

    packages = find_packages(exclude=['demo']),
    include_package_data = True,
    zip_safe=False,

    license = "BSD",
    keywords = "django application authentication authorization",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
