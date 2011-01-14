django-janitor
==============

Do you have existing django apps whose models store HTML content?  Do you want to
use bleach_ to clean that HTML, but you don't want to modifying the app? If so,
django-janitor may be useful for you.

Installation
------------

**This software is not yet ready for production use**! However, if you want to 
test it out, just put the contents of the janitor directory in a Django project,
and add ``janitor`` to ``INSTALLED_APPS``, then run ``manage.py syncdb``

Usage
-----

Once installed, you would then use Django's Admin to create a FieldSanitizer, 
which consists of a ContentType and a field name.  At that point, django-janitor
listens for the pre_save signal for the Model that corresponds to the selected
ContentType, and the contents of the supplied ``field_name`` are run through bleach.

Here's a Screenshot: |screenshot|

.. _bleach: https://github.com/jsocol/bleach
.. |screenshot| image:: https://bitbucket.org/bkmontgomery/django-janitor/raw/0f97e4427c21/screenshot.png

