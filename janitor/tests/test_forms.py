from django.test import TestCase

from janitor.models import FieldSanitizer
from janitor.forms import FieldSanitizerAdminForm


class TestFieldSanitizerAdminForm(TestCase):
    def setUp(self):
        self.form = FieldSanitizerAdminForm()

    def test_form(self):
        self.assertEqual(self.form.Meta.model, FieldSanitizer)
        expected_fields = [
            'attributes',
            'content_type',
            'field_name',
            'strip',
            'strip_comments',
            'styles',
            'tags',
        ]
        self.assertEqual(sorted(self.form.fields), expected_fields)

    def test_expected_output(self):
        """Verify that the ContentTypeChoiceFieldWithAppLabel field displays
        things as expected."""
        # Assuming the auth/user content type is installed
        self.assertIn("auth/user", str(self.form))
