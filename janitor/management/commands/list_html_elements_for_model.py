"""
Management utility to clean a specific Model that is registered with a FieldSanitizer.
"""
from optparse import make_option
from django.core.management.base import CommandError, LabelCommand
from janitor.models import FieldSanitizer, _clean_class_objects, _get_tags_used_in_content

class Command(LabelCommand):

    help = "Lists HTML elements used in a Model with a related FieldSanitizer"
    args = "[appname.modelname]"
    label = 'application name.model name'

    can_import_settings = False
   
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
       
        # BaseCommand doesn't have stdout included in Django < 1.2 
        # So, let's add it in if it's not already there.
        if not hasattr(self, 'stdout'):
            from sys import stdout
            self.stdout = stdout

    def handle_label(self, label, **options):
        try:
            app_label, model = label.lower().split('.')
        except ValueError:
            raise CommandError("Invalid app_label.model_name: %s" % label)
        
        tag_list = _get_tags_used_in_content(app_label, model)
        self.stdout.write("\nTags used in content:\n\n    %s\n\n" % '\n    '.join(tag_list))
