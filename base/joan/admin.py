from __future__ import unicode_literals

from import_export import resources, fields, widgets
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from import_export.admin import ImportExportMixin, ImportExportModelAdmin

from django.contrib import admin
from django.db.models import Count
from django.contrib.admin import SimpleListFilter

from .models import Requirement
from .models import Feature
from .models import Ticket
from .models import Agreement
from .models import Project
from .models import Release



class FeatureResource(resources.ModelResource):

    project = fields.Field(column_name="Project",attribute="project",widget=ForeignKeyWidget(Project,"project_name"))
    requirement = fields.Field(column_name="Requirement",attribute="requirement",widget=ManyToManyWidget(Requirement,",","reqd_id"))
    release = fields.Field(column_name="Release",attribute="release",widget=ForeignKeyWidget(Release,"release_name"))
    feature_heading = fields.Field(column_name="Category", attribute="feature_heading")
    feature_text = fields.Field(column_name="Feature", attribute="feature_text")

    class Meta:
        model = Feature
        import_id_fields = ('id',)
        exclude = ['created_at', 'updated_at', 'feature_detail',]
        fields = ['id', 'project', 'requirement', 'release','feature_heading', 'feature_text']


    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        dataset.insert_col(0, col=["",]*dataset.height, header="id")

    def get_instance(self, instance_loader, row):
        return False





def get_admin_url(model,param):
    return "/admin/joan/"+model+"/%d/" %param.id



class ProjectFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Project'

    #Parameter for the filter that will be used in the URL query.
    parameter_name = 'project'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        projects = set([p for p in Project.objects.all()])
        return [(p.id, p.project_name) for p in projects]


    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

        if self.value():
            return queryset.filter(release__project__id__exact=self.value())

        else:
            return queryset

class RequirementAdmin(admin.ModelAdmin):

    def requirement(self):
        return self.reqd_id + " " + self.requirement_heading

    def get_queryset(self, request):
        qs = super(RequirementAdmin, self).get_queryset(request)
        return qs.annotate(feature_count=Count('feature'))

    def show_feature_count(self, inst):
        return inst.feature_count

    def project(self):
        return Project.objects.filter(release__id__exact=self.release.id)

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
    list_display = [requirement, features]
    list_filter = [ProjectFilter]


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

    list_display = ["feature_text", "feature_heading", requirements]
    list_filter = [ProjectFilter]





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


class ReleaseInline(admin.TabularInline):
    model = Release


class ProjectAdmin(admin.ModelAdmin):

    inlines = [
        ReleaseInline,
    ]

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
