from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save

from bleach import Bleach

def _register(callback, content_type_list):
    for ct in content_type_list:
        pre_save.connect(callback, sender=ct.model_class(), dispatch_uid=ct.model)

class FieldSanitizer(models.Model):
    content_type = models.ForeignKey(ContentType)
    field_name = models.CharField(max_length=255, help_text="The name of a field in the selected Model. It probably should be a TextField or some sublcass of TextField.")
    # It sure would be nifto to pass this into Bleach.
    #tags =     
    #attributes =

    def __unicode__(self):
        return u"%s - %s" % (self.content_type, self.field_name)

    class Meta:
        ordering = ['content_type', 'field_name', ]
        unique_together = (('content_type', 'field_name'), )

    def save(self, *args, **kwargs):
        assert self._field_name_in_model(), "The field_name '%s' does not exist in the model '%s'" % (self.field_name, self.content_type.model)
        super(FieldSanitizer, self).save(*args, **kwargs)
        # Register the signal with the specified model.
        _register(sanitize_fields, [self.content_type])

    def _field_name_in_model(self):
        m = self.content_type.model_class()
        return self.field_name in [f.name for f in m._meta.fields]

def sanitize_fields(sender, **kwargs):
    """
    The signal handler for a FieldSanitizer

    ``sender`` - the model class
    ``instance`` - an instance of the sender
    ``tags`` - a list of tags to allow, e.g. ['b', 'em', 'strong']
    # Not yet avaiable: ``attributes`` - a list or dict of attributes to allow, e.g. ['href', ] or {'a': ['href']}

    Note: ``tags`` and ``attributes`` are passed directly into Bleach

    """
    sender_content_type = ContentType.objects.get_for_model(sender)
    sender_instance = kwargs['instance']
     
    bl = Bleach()

    sanitizers = FieldSanitizer.objects.filter(content_type=sender_content_type)
    for sanitizer in sanitizers:
        if hasattr(sender_instance, sanitizer.field_name):
            field_content = getattr(sender_instance, sanitizer.field_name)
            if 'tags' in kwargs:
                field_content = bl.clean(field_content, tags=kwargs['tags'])
            else:
                field_content = bl.clean(field_content)
            setattr(sender_instance, sanitizer.field_name, new_content)

# Register everything
_content_type_ids = FieldSanitizer.objects.values_list('content_type').distinct()
_content_types = [ct for ct in ContentType.objects.filter(id__in=_content_type_ids)]
_register(sanitize_fields, _content_types)
