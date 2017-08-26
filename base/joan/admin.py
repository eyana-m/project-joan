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

class FeatureInLine(admin.TabularInline):
    model = Feature

class RequirementAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(RequirementAdmin, self).get_queryset(request)
        return qs.annotate(feature_count=Count('feature'))

    def show_feature_count(self, inst):
        return inst.feature_count

    show_feature_count.short_description = "Related System Features"
    show_feature_count.admin_order_field = "feature_count"
    list_display = ["reqd_id", "requirement_heading", "show_feature_count"]

    inline=[FeatureInLine,]


def get_admin_url(param):
    return "/admin/joan/requirement/%d/" %param.id


class FeatureAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(FeatureAdmin, self).get_queryset(request)
        return qs.annotate(requirement_count=Count('requirement'))

    def show_requirement_count(self, inst):
        return inst.requirement_count

    def requirements(self):
        #html = ""
        temp = []
        for obj in Requirement.objects.filter(feature__id__exact=self.id):
            #temp.append(obj.reqd_id)
            temp.append('<a href="%s">%s</a>' %(get_admin_url(obj), obj.reqd_id))
        return temp
    requirements.allow_tags = True


    #list_filter = ['requirement']

    show_requirement_count.short_description = "Related Business Requirements"
    show_requirement_count.admin_order_field = "requirement_count"
    list_display = ["feature_text", "feature_heading","show_requirement_count", requirements]



admin.site.register(Requirement,RequirementAdmin)
admin.site.register(Feature,FeatureAdmin)
admin.site.register(Ticket)
