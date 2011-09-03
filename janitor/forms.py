from django.contrib.contenttypes.models import ContentType
from django.forms import ModelChoiceField, ModelForm
from models import FieldSanitizer

class ContentTypeChoiceFieldWithAppLabel(ModelChoiceField):
    """
    A ModelChoiceField for ContentTypes that displays the 
    app_label in addition to the name. 
    """
    def label_from_instance(self, obj):
        return "%s/%s" % (obj.app_label, obj.name)

class FieldSanitizerAdminForm(ModelForm):
    content_type = ContentTypeChoiceFieldWithAppLabel(ContentType.objects.all())
    class Meta:
        model = FieldSanitizer
