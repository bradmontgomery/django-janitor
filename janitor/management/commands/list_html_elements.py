"""
Management utility to list HTML elements used in Existing Content.
This could be useful when trying to decide which elements to include
in the whitelist.
"""
from django.core.management.base import BaseCommand
from janitor.models import _get_tags_used_in_content


class Command(BaseCommand):
    help = (
        "Lists HTML elements used in all Models that have "
        "a related FieldSanitizer"
    )

    def handle(self, *args, **options):
        tag_list = _get_tags_used_in_content()
        tag_list = ", ".join(sorted(tag_list))
        msg = "\nTags used in content: {0}\n"
        self.stdout.write(msg.format(tag_list))
