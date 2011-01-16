django-janitor
==============

Do you have existing django apps whose models store HTML content?  Do you want to
use bleach_ to clean that HTML, but you don't want to modifying the app? If so,
django-janitor may be useful for you.

Installation
------------

**This software is a work in progress, and is NOT ready for production usei!** i
However, if you want to try it out, just put the contents of the janitor directory 
in a Django project, and add ``janitor`` to ``INSTALLED_APPS``, then run ``manage.py syncdb``

Usage
-----

Once installed, you would then use Django's Admin to create a ``FieldSanitizer`` for 
all app Models with fields that contain HTML content.  The ``FieldSanitizer`` consists 
of a ``ContentType`` and a field name.  Once the ``FieldSanitizer`` is created, 
django-janitor listens for the pre_save signal for the Model that corresponds to the 
selected ContentType, and the contents of the supplied field name are cleaned with bleach.

Here's a Screenshot: |screenshot|

.. _bleach: https://github.com/jsocol/bleach
.. |screenshot| image:: https://bitbucket.org/bkmontgomery/django-janitor/raw/ab1b6a62be94/screenshot.png

