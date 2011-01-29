"""
Management utility to clean a specific Model that is registered with a FieldSanitizer.
"""
from optparse import make_option
from django.core.management.base import CommandError, LabelCommand
from janitor.models import FieldSanitizer, _clean_class_objects

class Command(LabelCommand):

    help = "Cleans fields for a specified Model"
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

        self.stdout.write("\nCleaning %s.%s\n" % (app_label, model))

        qs = FieldSanitizer.objects.filter(content_type__app_label=app_label, content_type__model=model)
        try:
            assert qs.count() > 0
        except AssertionError:
            raise CommandError("It looks like there are no FieldSanitizers defined for %s.%s" % (app_label, model)) 

        klass_list = [fs.content_type.model_class() for fs in qs]
        object_count = _clean_class_objects(klass_list)

        self.stdout.write("Cleaned %s Objects\n" % object_count)
