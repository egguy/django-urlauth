#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="django-urlauth-egguy",
    version="0.2.2",
    description="Django application for user authentication with key in hypertext link",
    url="https://github.com/egguy/django-urlauth/",
    author="Grigoriy Petukhov",
    author_email="lorien@lorien.name",
    packages=find_packages(exclude=["demo"]),
    include_package_data=True,
    zip_safe=False,
    license="BSD",
    keywords="django application authentication authorization",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
    install_requires=[
        "django>=1.11",
    ],
)
