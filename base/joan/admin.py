from __future__ import unicode_literals

from import_export import resources, fields, widgets
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from import_export.admin import ImportExportMixin, ImportExportModelAdmin

from django.contrib import admin
from django.db.models import Count
from django.contrib.admin import SimpleListFilter
from django import forms
from django.forms import ModelChoiceField

from .models import Requirement
from .models import Feature
from .models import Ticket
from .models import Agreement
from .models import Project
from .models import Release
from .models import Sprint



class FeatureResource(resources.ModelResource):

    #Ensure release model is within project context
    class ReleaseForeignKeyWidget(ForeignKeyWidget):
        def get_queryset(self, value, row):
            return self.model.objects.filter(
                release__project__project_name__exact=row["Project"],
                release_name__exact=row["Release"],
            )

    project = fields.Field(column_name="Project",attribute="project",widget=ForeignKeyWidget(Project,"project_name"))
    requirement = fields.Field(column_name="Requirement",attribute="requirements",widget=ManyToManyWidget(Requirement,",","reqd_id"))
    release = fields.Field(column_name="Release",attribute="release",widget=ReleaseForeignKeyWidget(Release,"release_name"))
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


class TicketResource(resources.ModelResource):

    ## Separate Release Column for Import.
    ## Ensure Release and Sprint is within project context
    class FullSprintForeignKeyWidget(ForeignKeyWidget):
        def get_queryset(self, value, row):
            return self.model.objects.filter(
                release__project__project_name__exact=row["Project"],
                release__release_name__exact=row["Release"],
                sprint_name__iexact=row["Sprint"]
            )

    project = fields.Field(column_name="Project",attribute="project",widget=ForeignKeyWidget(Project,"project_name"))
    features = fields.Field(column_name="Features",attribute="features",widget=ManyToManyWidget(Feature,"|","feature_text"))
    sprint = fields.Field(column_name="Sprint",attribute="sprint",widget=FullSprintForeignKeyWidget(Sprint,"sprint_name"))
    ticket_text = fields.Field(column_name="Ticket Text", attribute="ticket_text")
    ticket_id = fields.Field(column_name="Ticket ID", attribute="ticket_id")
    dev_assigned = fields.Field(column_name="Developer", attribute="dev_assigned")
    ticket_url = fields.Field(column_name="Link", attribute="ticket_url")
    is_feature = fields.Field(column_name="Is Feature", attribute="is_feature")


    class Meta:
        model = Ticket
        import_id_fields = ('id',)
        exclude = ['created_at', 'updated_at' ]
        fields = ['project', 'features', 'sprint', 'ticket_text', 'ticket_id', 'dev_assigned','ticket_url', 'is_feature']

    def dehydrate_sprint(self, ticket):
        return '%s - %s' % (ticket.sprint.release, ticket.sprint.sprint_name)

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


class RequirementForm(forms.ModelForm):

    class Meta:
        model = Requirement
        #fields = ['project', 'release', 'reqd_id', 'requirement_heading', 'requirement_text', 'requirement_details']
        exclude = ['created_at', 'updated_at']



class RequirementAdmin(admin.ModelAdmin):

    form = RequirementForm

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
        for obj in Feature.objects.filter(requirements__id__exact=self.id):
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

    list_display = ["feature_text", "feature_heading", requirements, "release",  "feature_status"]
    list_filter = [ProjectFilter, "release", "feature_status"]


class TicketAdmin(ImportExportMixin, admin.ModelAdmin):

    resource_class = TicketResource
    def features(self):
        temp = []
        for obj in Feature.objects.filter(ticket__id__exact=self.id):
            temp.append('<a href="%s">%s</a>' %(get_admin_url("feature",obj), obj.feature_text))
        if len(temp) >2:
            temp2 = temp[:2]
            temp2.append('<a href="/admin/joan/feature"> more</a>')
            return temp2
        else:
            return temp
        #return '<a href="%s" target="_blank">%s</a>' %(get_admin_url("feature",self.feature), self.feature.feature_text)


    features.allow_tags = True
    features.short_description = "Related Features"

    def pm_link(self):
        return '<a href="%s" target="_blank">%s</a>' %(self.ticket_url, self.ticket_id)

    pm_link.allow_tags = True
    pm_link.short_description = "PM Tool Link"


    list_display = ["ticket_text",pm_link, features, "sprint", "ticket_status"]


class ReleaseInline(admin.StackedInline):
    model = Release


    def get_extra (self, request, obj=None, **kwargs):
        """Dynamically sets the number of extra forms. 0 if the related object
        already exists or the extra configuration otherwise."""
        if obj:
            # Don't add any extra forms if the related object already exists.
            return 0
        return self.extra


class ProjectAdmin(admin.ModelAdmin):

    inlines = [
        ReleaseInline,
    ]

    def total_releases(self):
        return Release.objects.filter(project__id__exact=self.id).count()

    list_display = ["project_name", "project_company", total_releases]


class ReleaseAdmin(admin.ModelAdmin):
    list_display =  ["project_release"]



class SprintAdmin(admin.ModelAdmin):

    list_display = ["release_sprint", "project", "sprint_start_date", "sprint_end_date", "sprint_status"]


admin.site.register(Requirement,RequirementAdmin)
admin.site.register(Feature,FeatureAdmin)
admin.site.register(Ticket,TicketAdmin)
admin.site.register(Agreement)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Release, ReleaseAdmin)
admin.site.register(Sprint, SprintAdmin)
