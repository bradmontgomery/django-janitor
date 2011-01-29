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
To install the most recent release::

    pip install django-janitor

To install from the current repository::
    
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

Management Commands
-------------------

There are a few managment commands avaialable to make it easier to use django-janitor. The
first is ``clean_all`` which will look at all of the models that have a related Field Sanitizer, 
calling the models' ``save`` method to trigger the ``pre_save`` signal (which forces the fields
to be cleaned)::

    python manage.py clean_all

The second management command is ``clean_model``, which works in a similar fashion, but allows you
to specify an app and a model::

    python manage.py clean_model myapp.MyModel

Finally, ``list_html_elements`` and ``list_html_elements_for_model`` exist to help you discover what 
HTML elements are being used in existing content.  While these commands do require that a ``FieldSanitizer``
be configured for existing Models, they may be used to help you decide which tags to include in a whitelist.

You should run these commands before using ``clean_all`` or ``clean_model`` to see what sort of data 
exists before it's cleaned::

    python manage.py list_html_elements

Or::
    
    python manage.py list_html_elements_for_model myapp.MyModel

.. _bleach: https://github.com/jsocol/bleach
.. |screenshot| image:: https://bitbucket.org/bkmontgomery/django-janitor/raw/44f6deb56713/screenshot.png

