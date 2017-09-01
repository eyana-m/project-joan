from __future__ import unicode_literals

from import_export import resources
from import_export.admin import ImportExportMixin, ImportExportModelAdmin
from import_export import fields
from import_export import widgets

from django.contrib import admin
from django.db.models import Count

from .models import Requirement
from .models import Feature
from .models import Ticket
from .models import Agreement
from .models import Project
from .models import Release

class FeatureResource(resources.ModelResource):

    project = fields.Field(column_name="Project")
    requirement = fields.Field(column_name="Requirement")
    release = fields.Field(column_name="Release")
    feature_heading = fields.Field(column_name="Category")
    feature_text = fields.Field(column_name="Feature Name")

    class Meta:
        model = Feature
        exclude = ('id', 'created_at', 'updated_at', 'feature_detail',)

    def dehydrate_requirement(self, feature):
        temp = []
        for x in feature.requirement.all():
            temp.append(x.reqd_id)
        return ', '.join(temp)

    def dehydrate_project(self, feature):
        return feature.project.project_name

    def dehydrate_release(self, feature):
        temp = []
        for x in feature.requirement.all():
            temp.append(str(x.release))
        temp2 = list(set(temp))
        return ', '.join(temp2)

    def dehydrate_feature_heading(self, feature):
        return feature.feature_heading

    def dehydrate_feature_text(self, feature):
        return feature.feature_text



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

        if len(temp) >2:
            temp2 = temp[:2]
            temp2.append('<a href="/admin/joan/feature"> more</a>')
            return temp2
        else:
            return temp

    features.allow_tags = True
    features.short_description = "Related System Features"

    show_feature_count.short_description = "Feature Count"
    show_feature_count.admin_order_field = "feature_count"
    list_display = [requirement, "show_feature_count", features]


class FeatureAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = FeatureResource
    def requirements(self):
        temp = []
        for obj in Requirement.objects.filter(feature__id__exact=self.id):
            temp.append('<a href="%s">%s</a>' %(get_admin_url("requirement",obj), obj.reqd_id))
        return temp

    requirements.allow_tags = True
    requirements.short_description = "Related Requirements"

    def tickets(self):
        temp = []
        for obj in Ticket.objects.filter(feature__id__exact=self.id):
            temp.append('<a href="%s">%s</a>' %(get_admin_url("ticket",obj), obj.ticket_id))
        return temp

    tickets.allow_tags = True
    tickets.short_description = "Related Tickets"

    list_display = ["feature_text", "feature_heading", requirements, tickets]




class TicketAdmin(admin.ModelAdmin):
    def requirements(self):
        temp = []
        for obj in Requirement.objects.filter(feature__id__exact=self.feature.id):
            temp.append('<a href="%s">%s</a>' %(get_admin_url("requirement",obj), obj.reqd_id))
        return temp

    requirements.allow_tags = True
    requirements.short_description = "Related Requirements"

    def pm_link(self):
        return '<a href="%s" target="_blank">%s</a>' %(self.ticket_url, self.ticket_id)

    pm_link.allow_tags = True
    pm_link.short_description = "PM Tool Link"


    list_display = ["ticket_text", "release_sprint",pm_link, requirements]


class ProjectAdmin(admin.ModelAdmin):

    def total_releases(self):
        return Release.objects.filter(project__id__exact=self.id).count()


    #total_requirements.short_description = "Requirements"

    list_display = ["project_name", "project_company", total_releases]


class ReleaseAdmin(admin.ModelAdmin):
    list_display =  ["project_release"]


admin.site.register(Requirement,RequirementAdmin)
admin.site.register(Feature,FeatureAdmin)
admin.site.register(Ticket,TicketAdmin)
admin.site.register(Agreement)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Release, ReleaseAdmin)
