"""
Management utility to clean Models that are registered with a FieldSanitizer.

"""
from django.core.management.base import BaseCommand
from janitor.models import FieldSanitizer, _clean_class_objects


class Command(BaseCommand):
    help = "Cleans all Models that have a related FieldSanitizer"

    def handle(self, *args, **options):
        sanitizers = FieldSanitizer.objects.all()
        klass_list = [fs.content_type.model_class() for fs in sanitizers]
        updated = _clean_class_objects(klass_list)
        self.stdout.write("\nCleaned {0} Objects\n".format(updated))
