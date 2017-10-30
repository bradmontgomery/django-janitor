"""
Management utility to clean a specific Model that is registered with a
FieldSanitizer.

"""
from django.core.management.base import CommandError, LabelCommand
from janitor.models import FieldSanitizer, _clean_class_objects


class Command(LabelCommand):
    help = "Cleans fields for a specified Model"
    args = "[appname.modelname]"
    label = 'application name.model name'

    def handle_label(self, label, **options):
        try:
            app_label, model = label.lower().split('.')
        except ValueError:
            raise CommandError(
                "Invalid app_label.model_name: {0}".format(label)
            )

        self.stdout.write("\nCleaning {0}.{1}\n".format(app_label, model))

        qs = FieldSanitizer.objects.filter(
            content_type__app_label=app_label,
            content_type__model=model
        )
        try:
            assert qs.count() > 0
        except AssertionError:
            msg = "There are no FieldSanitizers defined for {0}.{1}"
            raise CommandError(msg.format(app_label, model))

        klass_list = [fs.content_type.model_class() for fs in qs]
        object_count = _clean_class_objects(klass_list)
        self.stdout.write("Cleaned {0} Objects\n".format(object_count))
