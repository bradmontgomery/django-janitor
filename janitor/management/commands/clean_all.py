"""
Management utility to clean Models that are registered with a FieldSanitizer.
"""

from django.core.management.base import NoArgsCommand
from janitor.models import FieldSanitizer, _clean_class_objects

class Command(NoArgsCommand):

    help = "Cleans all Models that have a related FieldSanitizer"

    def handle_noargs(self, **options):
        klass_list = [fs.content_type.model_class() for fs in FieldSanitizer.objects.all()]
        object_count = _clean_class_objects(klass_list)

        self.stdout.write("\nCleaned %s Objects\n" % object_count)
