"""
This module contains various lists of HTML tags that 
can be used as a  whitelist for Bleach.

"""
structure_tags = ['div', 'span', ]
basic_content_tags = ['a','abbr', 'acronym', 'blockquote', 'cite', 'code', 'dd', 'del', 'dfn', 'dl', 'dt', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'img', 'ins', 'kbd', 'li', 'ol', 'p', 'pre', 'q', 'samp', 'strong', 'ul', ]
table_tags = ['caption','col', 'colgroup', 'table', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr', ]
form_tags = ['button', 'fieldset', 'form', 'input', 'label', 'legend', 'optgroup', 'option', 'select', 'textarea', ]
script_tags = ['script', 'noscript', ]

# The Whole Shebang, as listed at http://htmldog.com/reference/htmltags/
the_whole_shebang = ['a','abbr', 'acronym', 'address', 'area', 'b', 'base', 'bdo', 'big', 'blockquote', 'body', 'br', 'button', 'caption', 'cite', 'code', 'col', 'colgroup', 'dd', 'del', 'dfn', 'div', 'dl', 'DOCTYPE', 'dt', 'em', 'fieldset', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'html', 'hr', 'i', 'img', 'input', 'ins', 'kbd', 'label', 'legend', 'li', 'link', 'map', 'meta', 'noscript', 'object', 'ol', 'optgroup', 'option', 'p', 'param', 'pre', 'q', 'samp', 'script', 'select', 'small', 'span', 'strong', 'style', 'sub', 'sup', 'table', 'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 'title', 'tr', 'tt', 'ul', 'var', ]

# A very small whitelist of HTML Attributes
attributes = ['alt', 'class', 'href', 'id', 'src', 'title',]
