from django.contrib import admin
from . import models


@admin.register(models.Log)
class AuditTrailAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in models.Log._meta.get_fields()
    ]
