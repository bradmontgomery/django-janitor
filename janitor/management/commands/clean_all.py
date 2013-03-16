"""
Management utility to clean Models that are registered with a FieldSanitizer.
"""
from django.core.management.base import NoArgsCommand
from janitor.models import FieldSanitizer, _clean_class_objects


class Command(NoArgsCommand):

    help = "Cleans all Models that have a related FieldSanitizer"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        # BaseCommand doesn't have stdout included in Django < 1.2
        # So, let's add it in if it's not already there.
        if not hasattr(self, 'stdout'):
            from sys import stdout
            self.stdout = stdout

    def handle_noargs(self, **options):
        sanitizers = FieldSanitizer.objects.all()
        klass_list = [fs.content_type.model_class() for fs in sanitizers]
        object_count = _clean_class_objects(klass_list)

        self.stdout.write("\nCleaned {0} Objects\n".format(object_count))
