from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Requirement, Feature, Ticket, Project, Release, Sprint
from datetime import timedelta, date
from django.utils.timezone import localtime, now
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.http import HttpResponse

def count_business_days(from_date, to_date):
    day_generator = (from_date + timedelta(x + 1) for x in range((to_date - from_date).days))
    return sum(1 for day in day_generator if day.weekday() < 5)

def percentage(part, whole):
    try: return "{:.0%}".format(part/whole)
    except: return '0%'

#Add HTML decorators soon!
def get_requirements_status(done, project):
    if Requirement.objects.distinct().filter(project__id__exact=project).count() == done.count():
        status = "Complete"
    else:
        status = "Ongoing"
    return status



# List of Projects
class IndexView(generic.ListView):
    template_name = 'joan/index.html'
    context_object_name = 'latest_project_list'

    def get_queryset(self):
        return Project.objects.order_by('id')[:10]


# List of Requirements by Release under the Project
class ProjectView(generic.DetailView):
    model = Project
    template_name = 'joan/project.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProjectView, self).get_context_data(**kwargs)
        current_sprint = Sprint.objects.filter(release__project__id__exact=self.kwargs['pk']).filter(sprint_status__exact='AC').get()
        context['current_sprint'] = current_sprint
        context['sprint_man_days_left'] = count_business_days(localtime(now()).date(),current_sprint.sprint_end_date)
        context['release_man_days_left'] = count_business_days(localtime(now()).date(),current_sprint.release.release_uat_start_date)
        context['sprint_list'] = Sprint.objects.filter(release__project__id__exact=self.kwargs['pk']).order_by('-sprint_end_date')

        context['features_count'] = Feature.objects.filter(release__project__id__exact=self.kwargs['pk']).count()

        context['features_done_count'] = Feature.objects.filter(release__project__id__exact=self.kwargs['pk']).filter(feature_status__exact='DO').count()
        context['features_done_percentage'] = percentage(context['features_done_count'],context['features_count'] )

        uc_done_only = Feature.objects.filter(release__project__id__exact=self.kwargs['pk']).filter(feature_status__exact='DU').count()
        context['features_uc_done_count'] = context['features_done_count'] + uc_done_only
        context['features_uc_done_percentage'] = percentage(context['features_uc_done_count'] ,context['features_count'])

        context['features_for_fv_count'] = Feature.objects.filter(release__project__id__exact=self.kwargs['pk']).filter(feature_status__exact='FV').count()
        context['features_for_fv_percentage'] = percentage(context['features_for_fv_count'],context['features_uc_done_count'])

        requirements_count = Requirement.objects.filter(project__id__exact=self.kwargs['pk']).count()
        context['requirements_met_count'] = Requirement.objects.filter(project__id__exact=self.kwargs['pk']).filter(feature__feature_status__exact='DO').distinct().count()

        context['requirements_met_percentage'] = percentage(context['requirements_met_count'],requirements_count)
        return context

class RequirementView(generic.DetailView):
    model = Requirement
    template_name = 'joan/requirement.html'

class FeatureView(generic.DetailView):
    model = Feature
    template_name = 'joan/feature.html'


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FeatureView, self).get_context_data(**kwargs)
        context['requirement_list'] = Requirement.objects.filter(feature__id__exact=self.kwargs['pk'])
        #context['releases'] = list(set(Requirement.objects.filter(feature__id__exact=self.kwargs['pk']).values_list('release', flat=True)))
        return context

class ReleaseView(generic.DetailView):
    model = Release
    template_name = 'joan/release.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ReleaseView, self).get_context_data(**kwargs)
        context['requirement_list'] = Requirement.objects.filter(feature__release__id__exact=self.kwargs['pk']).distinct()

        # Select all requirements where all features are done
        context['done_requirement_list'] = Requirement.objects.distinct().filter(feature__release__id__exact=self.kwargs['pk']).filter(feature__feature_status__exact='DO').exclude(feature__feature_status__in=('NW', 'DU', 'FV'))

        context['done_feature_list'] = Feature.objects.filter(release__id__exact=self.kwargs['pk']).filter(feature_status__exact='DO')

        context['done_feature_list'] = Feature.objects.filter(release__id__exact=self.kwargs['pk']).filter(feature_status__exact='DO')

        context['done_sprint_list'] = Sprint.objects.filter(release__id__exact=self.kwargs['pk']).filter(sprint_status__exact='DO')

        context['sprint_list'] = Sprint.objects.filter(release__id__exact=self.kwargs['pk']).order_by('-sprint_end_date')

        return context

class ProjectRequirementsView(generic.DetailView):
    model = Project
    template_name = 'joan/requirements_list.html'



    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProjectRequirementsView, self).get_context_data(**kwargs)

        # Select all requirements where all features are done
        context['done_requirement_list'] = Requirement.objects.distinct().filter(project__id__exact=self.kwargs['pk']).filter(feature__feature_status__exact='DO').exclude(feature__feature_status__in=('NW', 'DU', 'FV'))
        context['ongoing_requirements_count'] = Requirement.objects.distinct().filter(project__id__exact=self.kwargs['pk']).filter(feature__feature_status__in=('NW', 'DU', 'FV')).count() + Requirement.objects.distinct().filter(project__id__exact=self.kwargs['pk']).filter(feature__feature_status__isnull=True).count()
        context['requirements_status'] = get_requirements_status(context['done_requirement_list'],self.kwargs['pk'])
        return context

class ProjectFeaturesView(generic.DetailView):
    model = Project
    template_name = 'joan/features_list.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProjectFeaturesView, self).get_context_data(**kwargs)
        context['all_features'] = Feature.objects.distinct().filter(release__project__id__exact=self.kwargs['pk'])
        context['done_feature_list'] = Feature.objects.distinct().filter(release__project__id__exact=self.kwargs['pk']).filter(feature_status__exact='DO')
        context['ongoing_features_count'] = Feature.objects.distinct().filter(release__project__id__exact=self.kwargs['pk']).filter(feature_status__in=('NW', 'DU', 'FV')).count() + Feature.objects.distinct().filter(release__project__id__exact=self.kwargs['pk']).filter(feature_status__isnull=True).count()
        context['features_status']= get_requirements_status(context['done_feature_list'],self.kwargs['pk'])
        return context

class SprintView(generic.DetailView):
    model = Sprint
    template_name = 'joan/sprint.html'
