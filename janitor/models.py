from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.db import DatabaseError
from django.db import transaction

from bleach import clean 
from html5lib import html5parser
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

    @property
    def app_name(self):
        """ return the name of the App to which this sanitizer is associated """
        return self.content_type.app_label
    
    @property
    def model_name(self):
        """ return the name of the Model to which this sanitizer is associated """
        return self.content_type.model

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

def _clean_class_objects(klass_list):
    """
    Cleans the content for all classes in the provided list.
    This is done by forcing each instance of the class to
    invoke it's ``save`` method.

    Returns the total number of objects saved.

    This function is used in the management commands.
    """
    object_count = 0
    for klass in klass_list:
        for object in klass.objects.all():
            object.save() 
            object_count += 1
    
    return object_count

def _get_tags_used_in_content(app_label=None, model=None):
    """
    Use html5lib's parser to get a list of HTML tags used in content
    associated with a FieldSanitizer.

    This can be useful when determining what to include in a whitelist,
    and is used in the ``list_html_elements`` and ``list_html_elements_for_model``
    management commands.

    """
    queryset = FieldSanitizer.objects.all()
    if app_label and model:
        queryset = queryset.filter(content_type__app_label=app_label, content_type__model=model)

    tag_list = []

    for fs in queryset:
        model_class = fs.content_type.model_class()
        content_list = model_class.objects.values_list(fs.field_name, flat=True)

        for content in content_list:
            doc = html5parser.parse(content)
            tag_list.extend([str(tag.name) for tag in doc if tag.name])

    tag_list = list(set(tag_list)) # remove duplicates
    tag_list.sort()
    return tag_list

@transaction.commit_manually
def register_everything():
    """
    This function attempts to register all ``FieldSanitizer`` instances
    with the ``sanitize_fields`` callback. 

    When you initially install this app and run ``syncdb``, the model 
    doesn't exist in the database. This raises a ``DatabaseError`` exception,
    and in some DBMSs (PostgreSQL) ``syncdb`` will refuse to continute if a
    transaction did not get commited successfully. Hence the reason for all 
    transaction managment stuff.
    """
    transaction.commit()
    try:
        _content_type_ids = FieldSanitizer.objects.values_list('content_type').distinct()
        _content_types = [ct for ct in ContentType.objects.filter(id__in=_content_type_ids)]
        _register(sanitize_fields, _content_types)
    except DatabaseError:
        transaction.rollback()
    else:
        transaction.commit()
register_everything() # try to register the signal callbacks when this file is loaded
