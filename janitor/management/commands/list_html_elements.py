"""
Management utility to list HTML elements used in Existing Content.
This could be useful when trying to decide which elements to include
in the whitelist.
"""

from django.core.management.base import NoArgsCommand
from janitor.models import _get_tags_used_in_content


class Command(NoArgsCommand):

    help = ("Lists HTML elements used in all Models that have a"
            "related FieldSanitizer")

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        # BaseCommand doesn't have stdout included in Django < 1.2
        # So, let's add it in if it's not already there.
        if not hasattr(self, 'stdout'):
            from sys import stdout
            self.stdout = stdout

    def _tag_output(self, tag_list):
        p = "- {0}\n"
        return ''.join(p.format(t) for t in tag_list)

    def handle_noargs(self, **options):
        tag_list = _get_tags_used_in_content()
        self.stdout.write(
            "\nTags used in content:\n{0}\n".format(self._tag_output(tag_list))
        )
