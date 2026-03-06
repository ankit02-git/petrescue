from django.contrib import admin
from .models import Pet, Favorite, SightingReport


admin.site.register(Pet)
admin.site.register(Favorite)


class SightingReportAdmin(admin.ModelAdmin):
    list_display = ("pet", "reporter", "message", "created_at")


admin.site.register(SightingReport, SightingReportAdmin)