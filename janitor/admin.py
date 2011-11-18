from django.contrib import admin
from forms import FieldSanitizerAdminForm
from models import FieldSanitizer

class FieldSanitizerAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'app_name', 'model_name', 'field_name', ) 
    form = FieldSanitizerAdminForm
admin.site.register(FieldSanitizer, FieldSanitizerAdmin)
