from __future__ import unicode_literals

from django.contrib import admin
from django.db.models import Count

from .models import Requirement
from .models import Feature
from .models import Ticket


def get_admin_url(model,param):
    return "/admin/joan/"+model+"/%d/" %param.id

class RequirementAdmin(admin.ModelAdmin):

    def requirement(self):
        return self.reqd_id + " " + self.requirement_heading

    def get_queryset(self, request):
        qs = super(RequirementAdmin, self).get_queryset(request)
        return qs.annotate(feature_count=Count('feature'))

    def show_feature_count(self, inst):
        return inst.feature_count

    def features(self):
        temp = []
        for obj in Feature.objects.filter(requirement__id__exact=self.id):
            temp.append('<a href="%s">%s</a>' %(get_admin_url("feature",obj), obj.feature_text))
        return temp

    features.allow_tags = True
    features.short_description = "Related System Features"

    show_feature_count.short_description = "Feature Count"
    show_feature_count.admin_order_field = "feature_count"
    list_display = [requirement, "show_feature_count", features]


class FeatureAdmin(admin.ModelAdmin):

    # Get Requirements Count

    # def get_queryset(self, request):
    #     qs = super(FeatureAdmin, self).get_queryset(request)
    #     return qs.annotate(requirement_count=Count('requirement'))
    #
    # def show_requirement_count(self, inst):
    #     return inst.requirement_count

    def requirements(self):
        temp = []
        for obj in Requirement.objects.filter(feature__id__exact=self.id):
            temp.append('<a href="%s">%s</a>' %(get_admin_url("requirement",obj), obj.reqd_id))
        return temp

    requirements.allow_tags = True
    requirements.short_description = "Related Business Requirements"


    list_display = ["feature_text", "feature_heading", requirements]



admin.site.register(Requirement,RequirementAdmin)
admin.site.register(Feature,FeatureAdmin)
admin.site.register(Ticket)
