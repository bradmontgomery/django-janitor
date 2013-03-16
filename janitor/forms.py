from django.contrib.contenttypes.models import ContentType
from django.forms import ModelChoiceField, ModelForm

from .models import FieldSanitizer


class ContentTypeChoiceFieldWithAppLabel(ModelChoiceField):
    """A ModelChoiceField for ContentTypes that displays the app_label in
    addition to the name.
    """
    def label_from_instance(self, obj):
        return u"{0}/{1}".format(obj.app_label, obj.name)


class FieldSanitizerAdminForm(ModelForm):
    content_type = ContentTypeChoiceFieldWithAppLabel(
        ContentType.objects.all().order_by('app_label', 'model')
    )

    class Meta:
        model = FieldSanitizer
