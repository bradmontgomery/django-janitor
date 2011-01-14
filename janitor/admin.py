from django.contrib import admin
from models import FieldSanitizer

class FieldSanitizerAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'field_name', ) 

admin.site.register(FieldSanitizer, FieldSanitizerAdmin)
