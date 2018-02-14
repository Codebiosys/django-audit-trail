from django.contrib import admin
from . import models


@admin.register(models.AuditLog)
class AuditingAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in models.AuditLog._meta.get_fields()
    ]
