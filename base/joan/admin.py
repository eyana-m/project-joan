from __future__ import unicode_literals

from django.contrib import admin
from django.db.models import Count

from .models import Requirement
from .models import Feature
from .models import Ticket
from .models import Agreement
from .models import Project


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


class FeatureAdmin(admin.ModelAdmin):
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


    list_display = ["release", "iteration", "ticket_text", pm_link, requirements]


class ProjectAdmin(admin.ModelAdmin):

    def total_requirements(self):
        return Requirement.objects.filter(project__id__exact=self.id).count()


    total_requirements.short_description = "Requirements"

    list_display = ["project_name", "project_company", total_requirements]


admin.site.register(Requirement,RequirementAdmin)
admin.site.register(Feature,FeatureAdmin)
admin.site.register(Ticket,TicketAdmin)
admin.site.register(Agreement)
admin.site.register(Project, ProjectAdmin)
