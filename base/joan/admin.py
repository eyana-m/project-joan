from __future__ import unicode_literals

from django.contrib import admin
from django.db.models import Count

from .models import Requirement

from .models import Feature

from .models import Ticket

# class ChildInline(admin.TabularInline):
#     model = Feature
#
# class ParentAdmin(admin.ModelAdmin):
#     inlines = [
#         ChildInline,
#     ]
#
#
# admin.site.register(Feature)


class RequirementAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(RequirementAdmin, self).get_queryset(request)
        return qs.annotate(feature_count=Count('feature'))

    def show_feature_count(self, inst):
        return inst.feature_count

    show_feature_count.short_description = "Related Features"
    show_feature_count.admin_order_field = "feature_count"
    list_display = ["reqd_id", "requirement_heading", "show_feature_count"]

class FeatureAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(FeatureAdmin, self).get_queryset(request)
        return qs.annotate(requirement_count=Count('requirement'))

    def show_requirement_count(self, inst):
        return inst.requirement_count

    show_requirement_count.short_description = "Related Requirements"
    show_requirement_count.admin_order_field = "requirement_count"
    list_display = ["feature_text", "feature_heading","show_requirement_count"]


admin.site.register(Requirement,RequirementAdmin)
admin.site.register(Feature,FeatureAdmin)
admin.site.register(Ticket)
