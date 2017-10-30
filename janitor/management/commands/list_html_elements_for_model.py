"""
Management utility to clean a specific Model that is registered with a
FieldSanitizer.
"""
from django.core.management.base import CommandError, LabelCommand
from janitor.models import _get_tags_used_in_content


class Command(LabelCommand):
    help = "Lists HTML elements used in a Model with a related FieldSanitizer"
    args = "[appname.modelname]"
    label = 'application name.model name'

    def handle_label(self, label, **options):
        try:
            app_label, model = label.lower().split('.')
        except ValueError:
            raise CommandError("Invalid app_label.model_name: {0}".format(label))

        tag_list = _get_tags_used_in_content(app_label, model)
        tag_list = ", ".join(sorted(tag_list))
        msg = "\nTags used in {}.{}: {}\n".format(app_label, model, tag_list)
        self.stdout.write(msg)
