========
Overview
========

django-janitor allows you to use bleach_ to clean HTML stored in a Model's field.

Features
--------
* You don't need to edit an existing app (django-janitor listens for a Models' pre_save signal)
* Allowed HTML tags, attributes, and css are specified in a whitelist
* Whitelists are managed in Django's Admin
* There are (sensible) default whitelists included
* Works with Bleach 0.5.0

Installation
------------

**This software is a work in progress, and is NOT yet ready for widespread use!**

However, if you want to try it out, just put the contents of the janitor directory
in a Django project, and add ``janitor`` to ``INSTALLED_APPS``, then run ``manage.py syncdb``

Usage
-----

Browse to the Janitor app in Django's Admin, and create a new Field sanitizer. Then 
select the Model and specify the fieldname which should be cleaned. After you set up 
the whitelists for Tags, Attributes, etc, save the Field sanitizer.

Then, when you save the Model to which the Field Sanitizer is associated, the content 
in the specified field will be cleaned using bleach_.

Here's a Screenshot: |screenshot|

.. _bleach: https://github.com/jsocol/bleach
.. |screenshot| image:: https://bitbucket.org/bkmontgomery/django-janitor/raw/44f6deb56713/screenshot.png

