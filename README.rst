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
To install the most recent release:

    pip install django-janitor

To install from the current repository:
    
    pip intall hg+https://bitbucket.org/bkmontgomery/django-janitor/

Usage
-----

Browse to the Janitor app in Django's Admin, and create a new Field sanitizer. Then 
select the Model and specify the fieldname which should be cleaned. After you set up 
the whitelists for Tags, Attributes, etc, save the Field sanitizer.

Then, when you save the Model to which the Field Sanitizer is associated, the content 
in the specified field will be cleaned using bleach_.

Here's a Screenshot: 

|screenshot|

.. _bleach: https://github.com/jsocol/bleach
.. |screenshot| image:: https://bitbucket.org/bkmontgomery/django-janitor/raw/44f6deb56713/screenshot.png

