# django-urlauth

This is a maintenance fork of the original django-urlauth by Grigoriy Petukhov.

This django application allows you to build special links.
When somebody goes via that link to your site, it will be automatically authenticated.
THis is achieved with special GET arguments which are appended to the link.
Such links are usually used in the emails.

Example of such link: http://domain.com/profile/edit/?authkey=SOME_HASH

For installation instructions, see the file "INSTALL".

Full documentation is available in the file "index.rst" in the "docs/" directory.


## Changes in this fork

- Updated to work with Django 1.11+
- Added support for Python 3.6+
- Added tests runner
