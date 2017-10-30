from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from janitor import whitelists
from janitor.models import FieldSanitizer


class TestJanitor(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Hack: Use the FieldSanitizer models as the target, so we get a
        # field sanitizer that cleans other field sanitizers' syles field.
        cls.ct = ContentType.objects.get_for_model(FieldSanitizer)
        cls.fs = FieldSanitizer.objects.create(
            content_type=cls.ct,
            field_name="styles",
            tags="h1, p, a",
            attributes="href",
            styles="",
            strip=True,
            strip_comments=True,
        )

        # some content that we'll try to clean
        cls.sample_content = ("""
<h1 id="a"><a href="/">Heading</a></h1>
<p style="color:blue;" class="foo">Blue <strong>text</strong>
<script></script></p>
        """)

        # Cleaned results to verify that everything's working
        cls.cleaned_content = ("""
<h1><a href="/">Heading</a></h1>
<p>Blue text
</p>
        """)

    def setUp(self):
        self.obj = FieldSanitizer.objects.create(
            content_type=self.ct,
            field_name="field_name",
            styles=self.sample_content
        )

    def tearDown(self):
        self.obj.delete()

    def test__str__(self):
        """Tests the FieldSanitizer.__str__ method."""
        self.assertEqual(self.fs.__str__(), "field sanitizer - styles")

    def test_app_name(self):
        self.assertEqual(self.fs.app_name, "janitor")

    def test_model_name(self):
        self.assertEqual(self.fs.model_name, "fieldsanitizer")

    def test__field_name_in_model(self):
        self.assertTrue(self.fs._field_name_in_model())

    def test__split(self):
        self.assertEqual(self.fs._split("a,b,c,"), ['a', 'b', 'c'])

    def test_get_tags_list(self):
        self.assertEqual(self.fs.get_tags_list(), ['h1', 'p', 'a'])

    def test_get_attributes_list(self):
        self.assertEqual(self.fs.get_attributes_list(), ['href'])

    def test_get_styles_list(self):
        self.assertEqual(self.fs.get_styles_list(), [])

    def test_default_clean(self):
        """Creates an instance of the test model with some sample content,
        then verifies that it gets cleaned upon saving.
        """
        self.assertEqual(self.obj.styles, self.cleaned_content)

    def test_get_bleach_clean_args(self):
        actual = self.fs.get_bleach_clean_args()
        expected = {
            'tags': ['h1', 'p', 'a'],
            'attributes': ['href'],
            'styles': [],
            'strip': True,
            'strip_comments': True,
        }
        self.assertDictEqual(actual, expected)

    def test_strip_content(self):
        """Adds an HTML comment to the class's sample content, then verifies
        that it gets removed.
        """
        self.obj.styles = "<!-- Hello! -->" + self.sample_content
        self.obj.save()
        self.assertEqual(self.obj.styles, self.cleaned_content)

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
