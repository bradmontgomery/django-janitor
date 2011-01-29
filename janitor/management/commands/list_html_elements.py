"""
Management utility to list HTML elements used in Existing Content.
This could be useful when trying to decide which elements to include
in the whitelist.
"""

from django.core.management.base import NoArgsCommand
from janitor.models import FieldSanitizer, _clean_class_objects, _get_tags_used_in_content

class Command(NoArgsCommand):

    help = "Lists HTML elements used in all Models that have a related FieldSanitizer"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        # BaseCommand doesn't have stdout included in Django < 1.2 
        # So, let's add it in if it's not already there.
        if not hasattr(self, 'stdout'):
            from sys import stdout
            self.stdout = stdout
 
    def handle_noargs(self, **options):
        tag_list = _get_tags_used_in_content()
        self.stdout.write("\nTags used in content:\n\n    %s\n\n" % '\n    '.join(tag_list))
