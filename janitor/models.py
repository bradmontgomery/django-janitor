from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.db.utils import DatabaseError

from bleach import clean 
from janitor import whitelists

def _register(callback, content_type_list):
    for ct in content_type_list:
        pre_save.connect(callback, sender=ct.model_class(), dispatch_uid=ct.model)

def _j(some_list):
    return ', '.join(some_list)

class FieldSanitizer(models.Model):
    content_type = models.ForeignKey(ContentType)
    field_name = models.CharField(max_length=255, help_text="The name of a field in the selected Model. It probably should be a TextField or some sublcass of TextField.")
    tags = models.TextField(blank=True, default=_j(whitelists.basic_content_tags), help_text="A comma-separated whitelist of HTML tags that are allowed in the selected field")
    attributes = models.TextField(blank=True, default=_j(whitelists.attributes), help_text="A comma-separated whitelist of attributes that are allowed in the selected field")
    styles = models.TextField(blank=True, help_text="A comma-separated whitelist of allowed CSS properties within a style attribute. NOTE: For this to work, 'style' must be in the list of attributes.")
    strip = models.BooleanField(default=False, help_text="Strip disallowed HTML instead of escaping it.")
    strip_comments = models.BooleanField(default=True, help_text="Strip HTML comments.")

    def __unicode__(self):
        return u"%s - %s" % (self.content_type, self.field_name)

    class Meta:
        ordering = ['content_type', 'field_name', ]
        unique_together = (('content_type', 'field_name'), )

    def save(self, *args, **kwargs):
        """
        Checks to see that ``field_name`` is an attribute of the selected Model,
        then registers the signal handler with the appropriate model.
        """
        assert self._field_name_in_model(), "The field_name '%s' does not exist in the model '%s'" % (self.field_name, self.content_type.model)
        super(FieldSanitizer, self).save(*args, **kwargs)
        _register(sanitize_fields, [self.content_type]) 

    def _field_name_in_model(self):
        m = self.content_type.model_class()
        return self.field_name in [f.name for f in m._meta.fields]

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if len(tag.strip()) > 0]

    def get_attributes_list(self):
        return [attr.strip() for attr in self.attributes.split(',') if len(attr.strip()) > 0]

    def get_styles_list(self):
        return [s.strip() for s in self.styles.split(',') if len(s.strip()) > 0]

    def get_bleach_clean_args(self):
        """ Return a dict appropriate for passing into ``bleach.clean`` """
        return {'tags': self.get_tags_list(),
                'attributes':self.get_attributes_list(),
                'styles':self.get_styles_list(),
                'strip':self.strip,
                'strip_comments':self.strip_comments }

def sanitize_fields(sender, **kwargs):
    """
    The signal handler for a FieldSanitizer

    ``sender`` - the model class
    ``instance`` - an instance of the sender

    """
    sender_content_type = ContentType.objects.get_for_model(sender)
    sender_instance = kwargs['instance']
     
    for sanitizer in FieldSanitizer.objects.filter(content_type=sender_content_type):
        if hasattr(sender_instance, sanitizer.field_name):
            field_content = getattr(sender_instance, sanitizer.field_name)
            # Clean with bleach!
            field_content = clean(field_content, **sanitizer.get_bleach_clean_args())
            setattr(sender_instance, sanitizer.field_name, field_content)

try:
    # Register everything 
    _content_type_ids = FieldSanitizer.objects.values_list('content_type').distinct()
    _content_types = [ct for ct in ContentType.objects.filter(id__in=_content_type_ids)]
    _register(sanitize_fields, _content_types)
except DatabaseError:
    pass # FieldSanittizer's tables don't exist yet.
