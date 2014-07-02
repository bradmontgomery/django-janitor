from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.db import transaction
from django.db.models import loading
from django.test import TransactionTestCase

from janitor import whitelists
from janitor.models import FieldSanitizer
from janitor.models import _clean_class_objects, _get_tags_used_in_content
from janitor.tests.models import JanitorTestModel


class TestJanitor(TransactionTestCase):

    def setUp(self):
        transaction.commit()

        if 'janitor.tests' not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS = list(settings.INSTALLED_APPS)
            settings.INSTALLED_APPS.append('janitor.tests')
            loading.cache.loaded = False
            # This runs syncdb without running south migrations
            call_command('syncdb', verbosity=1, migrate=False)
        self.test_model = JanitorTestModel
        self.ct = ContentType.objects.get_for_model(JanitorTestModel)

        # some content that we'll try to clean
        self.sample_content = (
            """<h1 id="a"><a href="/">Heading</a></h1>"""
            """<p style="color:blue;" class="foo">Blue <strong>text</strong>"""
            """<script></script></p>"""
        )

        # Cleaned results to verify that everything's working
        self.cleaned_content = (
            """<h1 id="a"><a href="/">Heading</a></h1><p class="foo">Blue """
            """<strong>text</strong>&lt;script&gt;&lt;/script&gt;</p>"""
        )
        self.stripped_content = (
            """<h1 id="a"><a href="/">Heading</a></h1><p class="foo">Blue """
            """<strong>text</strong></p>"""
        )

    def tearDown(self):
        if 'janitor.tests' in settings.INSTALLED_APPS:
            JanitorTestModel.objects.all().delete()
            FieldSanitizer.objects.all().delete()
            settings.INSTALLED_APPS = list(settings.INSTALLED_APPS)
            settings.INSTALLED_APPS.remove('janitor.tests')

    def test__unicode__(self):
        """Tests the FieldSanitizer.__unicode__ method."""
        fs = FieldSanitizer(content_type=self.ct, field_name="content")
        self.assertEqual(fs.__unicode__(), "Janitor Test Model - content")

    def test_default_clean(self):
        """Creates an instance of the test model with some sample content,
        then verifies that it gets cleaned upon saving.
        """
        fs = FieldSanitizer(content_type=self.ct, field_name="content")
        fs.save()
        obj = self.test_model(content=self.sample_content)
        obj.save()
        self.assertEqual(obj.content, self.cleaned_content)
        self.assertEqual(fs.app_name, 'tests')
        self.assertEqual(fs.model_name, 'janitortestmodel')

    def test_strip_content(self):
        """Adds an HTML comment to the class's sample content, then verifies
        that it gets removed.
        """
        fs = FieldSanitizer(
            content_type=self.ct,
            field_name="content",
            strip=True,
            strip_comments=True
        )
        fs.save()
        obj = self.test_model(content="<!-- Hello! -->" + self.sample_content)
        obj.save()
        self.assertEqual(obj.content, self.stripped_content)

    def test_default_object_data(self):
        """Tests that FieldSanitizer's default tags, attributes, and clean_args
        are in place.
        """
        fs = FieldSanitizer()
        self.assertEqual(fs.get_tags_list(), whitelists.basic_content_tags)
        self.assertEqual(fs.get_attributes_list(), whitelists.attributes)

        expected_args = {
            'styles': [],
            'attributes': [u'alt', u'class', u'href', u'id', u'src', u'title'],
            'strip': False,
            'strip_comments': True,
            'tags': [
                u'a', u'abbr', u'acronym', u'blockquote', u'cite', u'code',
                u'dd', u'del', u'dfn', u'dl', u'dt', u'em', u'h1', u'h2',
                u'h3', u'h4', u'h5', u'h6', u'hr', u'img', u'ins', u'kbd',
                u'li', u'ol', u'p', u'pre', u'q', u'samp', u'strong', u'ul'
            ]
        }
        self.assertEqual(fs.get_bleach_clean_args(), expected_args)

    def test__clean_class_objects(self):
        """Runs the models._clean_class_objects function."""
        # This function returns the number of ojects saved/cleaned
        obj = JanitorTestModel(content="<p><x>Foo</x></p>")
        obj.save()

        self.assertEqual(_clean_class_objects([JanitorTestModel]), 1)

    def test__get_tags_used_in_content(self):
        JanitorTestModel.objects.create(
            content="<p><strong>Hi</strong><em>World</em></p>"
        )
        fs = FieldSanitizer(content_type=self.ct, field_name="content")
        fs.save()

        tags = sorted(_get_tags_used_in_content())
        self.assertEqual(tags, ['em', 'p', 'strong'])
