"""
Basic tests for django-janitor. 
"""
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.db.models import loading
from django.test import TestCase
from janitor.models import FieldSanitizer
from janitor import whitelists

class TestJanitor(TestCase):
    def setUp(self):
        if 'janitor.tests' not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS.append('janitor.tests')
            loading.cache.loaded = False
            call_command('syncdb', verbosity=0)
        from janitor.tests.models import TestModel
        self.test_model = TestModel
        self.ct = ContentType.objects.get_for_model(TestModel) 
        self.sample_content = """<h1 id="a"><a href="/">Heading</a></h1><p style="color:blue;" class="foo">Blue <strong>text</strong><script></script></p>"""
        self.cleaned_content = """<h1 id="a"><a href="/">Heading</a></h1><p class="foo">Blue <strong>text</strong>&lt;script&gt;&lt;/script&gt;</p>"""
        self.stripped_content = """<h1 id="a"><a href="/">Heading</a></h1><p class="foo">Blue <strong>text</strong></p>"""
    
    def tearDown(self):
        if 'janitor.tests' in settings.INSTALLED_APPS:
            from janitor.tests.models import TestModel
            TestModel.objects.all().delete()
            FieldSanitizer.objects.all().delete()
            settings.INSTALLED_APPS.remove('janitor.tests')

    def test_default_clean(self):  
        fs = FieldSanitizer(content_type=self.ct, field_name="content") 
        fs.save()
        obj = self.test_model(content=self.sample_content)
        obj.save()
        self.assertEqual(obj.content, self.cleaned_content)
        self.assertEqual(fs.app_name, 'tests')
        self.assertEqual(fs.model_name, 'testmodel')
        
    def test_strip_content(self):
        fs = FieldSanitizer(content_type=self.ct, field_name="content", strip=True, strip_comments=True)
        fs.save()
        obj = self.test_model(content="<!-- Hello! -->" + self.sample_content)
        obj.save()
        self.assertEqual(obj.content, self.stripped_content)
        
    def test_default_object_data(self):
        fs = FieldSanitizer()
        self.assertEqual(fs.get_tags_list(), whitelists.basic_content_tags)
        self.assertEqual(fs.get_attributes_list(), whitelists.attributes)

        expected_args = {'styles': [], 'attributes': [u'alt', u'class', u'href', u'id', u'src', u'title'], 'strip': False, 'strip_comments': True, 'tags': [u'a', u'abbr', u'acronym', u'blockquote', u'cite', u'code', u'dd', u'del', u'dfn', u'dl', u'dt', u'em', u'h1', u'h2', u'h3', u'h4', u'h5', u'h6', u'hr', u'img', u'ins', u'kbd', u'li', u'ol', u'p', u'pre', u'q', u'samp', u'strong', u'ul']}
        self.assertEqual(fs.get_bleach_clean_args(), expected_args)
