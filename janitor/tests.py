"""
Basic tests for janitor. 

"""

__test__ = {"doctest": """
Just test that FieldSanitizer's methods do what's expected, given 
default values. We can't really instantiate this, since we don't 
know what sort of models may exist.

>>> from janitor.models import FieldSanitizer

>>> fs = FieldSanitizer()

>>> fs.get_tags_list()
[u'a', u'abbr', u'acronym', u'blockquote', u'cite', u'code', u'dd', u'del', u'dfn', u'dl', u'dt', u'em', u'h1', u'h2', u'h3', u'h4', u'h5', u'h6', u'hr', u'img', u'ins', u'kbd', u'li', u'ol', u'p', u'pre', u'q', u'samp', u'strong', u'ul']

>>> fs.get_attributes_list()
[u'alt', u'class', u'href', u'id', u'src', u'title']

>>> fs.get_bleach_clean_args()
{'styles': [], 'attributes': [u'alt', u'class', u'href', u'id', u'src', u'title'], 'strip': False, 'strip_comments': True, 'tags': [u'a', u'abbr', u'acronym', u'blockquote', u'cite', u'code', u'dd', u'del', u'dfn', u'dl', u'dt', u'em', u'h1', u'h2', u'h3', u'h4', u'h5', u'h6', u'hr', u'img', u'ins', u'kbd', u'li', u'ol', u'p', u'pre', u'q', u'samp', u'strong', u'ul']}

"""}

