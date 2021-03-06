from html.parser import HTMLParser

from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction, IntegrityError
from django.db.models.signals import pre_save

from bleach import clean
from janitor import whitelists


def _register(callback, content_type_list):
    """Connects the `callback` function to each content type in the
    `content_type_list` with the `pre_save` signal handler."""
    for ct in content_type_list:
        pre_save.connect(
            callback,
            sender=ct.model_class(),
            dispatch_uid=ct.model
        )


def _j(some_list):
    """Shortcut for ``', '.join(some_list)``."""
    return ', '.join(some_list)


class FieldSanitizer(models.Model):
    content_type = models.ForeignKey(ContentType)
    field_name = models.CharField(
        max_length=255,
        help_text="The name of a field in the selected Model. It probably "
                  "should be a TextField or some sublcass of TextField."
    )
    tags = models.TextField(
        blank=True,
        default=_j(whitelists.basic_content_tags),
        help_text="A comma-separated whitelist of HTML tags that are allowed "
                  "in the selected field"
    )
    attributes = models.TextField(
        blank=True,
        default=_j(whitelists.attributes),
        help_text="A comma-separated whitelist of attributes that are "
                  "allowed in the selected field"
    )
    styles = models.TextField(
        blank=True,
        help_text="A comma-separated whitelist of allowed CSS properties "
                  "within a style attribute. NOTE: For this to work, 'style' "
                  "must be in the list of attributes."
    )
    strip = models.BooleanField(
        default=False,
        help_text="Strip disallowed HTML instead of escaping it."
    )
    strip_comments = models.BooleanField(
        default=True,
        help_text="Strip HTML comments."
    )

    def __str__(self):
        return "%s - %s" % (self.content_type, self.field_name)

    class Meta:
        ordering = ['content_type', 'field_name', ]
        unique_together = (('content_type', 'field_name'), )

    @property
    def app_name(self):
        """The name of the App to which this sanitizer is associated"""
        return self.content_type.app_label

    @property
    def model_name(self):
        """The name of the Model to which this sanitizer is associated """
        return self.content_type.model

    def save(self, *args, **kwargs):
        """Checks to see that ``field_name`` is an attribute of the selected
        Model, then registers the signal handler with the appropriate model.
        """
        msg = "The field_name '{0}' does not exist in the model '{1}'".format(
            self.field_name,
            self.content_type.model
        )
        assert self._field_name_in_model(), msg
        super().save(*args, **kwargs)
        _register(sanitize_fields, [self.content_type])

    def _field_name_in_model(self):
        m = self.content_type.model_class()
        return self.field_name in [f.name for f in m._meta.fields]

    def _split(self, text, delimiter=","):
        """Split text by delimiter and and filter out empty values."""
        items = [i.strip() for i in text.split(delimiter)]
        return list(filter(None, items))  # remove blanks

    def get_tags_list(self):
        return self._split(self.tags)

    def get_attributes_list(self):
        return self._split(self.attributes)

    def get_styles_list(self):
        return self._split(self.styles)

    def get_bleach_clean_args(self):
        """Return a dict appropriate for passing into ``bleach.clean``."""
        return {
            'tags': self.get_tags_list(),
            'attributes': self.get_attributes_list(),
            'styles': self.get_styles_list(),
            'strip': self.strip,
            'strip_comments': self.strip_comments
        }


def sanitize_fields(sender, **kwargs):
    """The signal handler for a FieldSanitizer

    * `sender` - the model class
    * `instance` - an instance of the sender

    """
    sender_content_type = ContentType.objects.get_for_model(sender)
    sender_instance = kwargs['instance']

    sanitizers = FieldSanitizer.objects.filter(content_type=sender_content_type)
    for sanitizer in sanitizers:
        if hasattr(sender_instance, sanitizer.field_name):
            field_content = getattr(
                sender_instance,
                sanitizer.field_name
            )
            # Clean with bleach!
            field_content = clean(
                field_content,
                **sanitizer.get_bleach_clean_args()
            )
            setattr(sender_instance, sanitizer.field_name, field_content)


def _clean_class_objects(klass_list):
    """Cleans the content for all classes in the provided list.
    This is done by forcing each instance of the class to
    invoke it's `save` method.

    Returns the total number of objects saved.

    This function is used in the management commands.
    """
    object_count = 0
    for klass in klass_list:
        for obj in klass.objects.all():
            obj.save()
            object_count += 1
    return object_count


class HTMLTagParser(HTMLParser):
    """A Simple parser that stores a set of tags in a document."""

    def add_tag(self, tag):
        if not hasattr(self, "tags"):
            self.tags = set()
        self.tags.add(tag)

    def handle_starttag(self, tag, attrs):
        self.add_tag(tag)


def _get_tags_used_in_content(app_label=None, model=None):
    """
    Use html5lib's parser to get a list of HTML tags used in content
    associated with a FieldSanitizer.

    This can be useful when determining what to include in a whitelist,
    and is used in the `list_html_elements` and
    `list_html_elements_for_model` management commands.

    """
    tag_parser = HTMLTagParser()
    queryset = FieldSanitizer.objects.all()
    if app_label and model:
        queryset = queryset.filter(
            content_type__app_label=app_label,
            content_type__model=model
        )

    for fs in queryset:
        model_class = fs.content_type.model_class()
        for content in model_class.objects.values_list(fs.field_name, flat=True):
            tag_parser.feed(content)

    return sorted(list(tag_parser.tags))


@transaction.atomic
def register_everything():
    """
    This function attempts to register all `FieldSanitizer` instances
    with the `sanitize_fields` callback.

    See: janitor.apps.JanitorConfig.ready()

    """
    try:
        with transaction.atomic():
            _content_type_ids = FieldSanitizer.objects.values_list('content_type')
            _content_type_ids = _content_type_ids.distinct()
            _content_types = [
                ct for ct in ContentType.objects.filter(id__in=_content_type_ids)
            ]
            _register(sanitize_fields, _content_types)
    except IntegrityError:
        transaction.rollback()
