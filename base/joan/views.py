from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Requirement, Feature, Ticket, Project, Release, Sprint

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
        context['current_sprint'] = Sprint.objects.filter(release__project__id__exact=self.kwargs['pk']).filter(sprint_status__exact='AC').get()
        context['sprint_list'] = Sprint.objects.filter(release__project__id__exact=self.kwargs['pk']).order_by('-sprint_end_date')
        context['features_count'] = Feature.objects.filter(release__project__id__exact=self.kwargs['pk']).count()
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
    #context['feature_list'] = Feature.objects.filter(requirements__in=context['requirement_list'],release__id__exact=self.kwargs['pk'])
        #context['feature_list'] = context['feature_list'].objects.filter()
        #context['releases'] = list(set(Requirement.objects.filter(feature__id__exact=self.kwargs['pk']).values_list('release', flat=True)))
        return context

class ProjectRequirementsView(generic.DetailView):
    model = Project
    template_name = 'joan/requirements_list.html'

class ProjectFeaturesView(generic.DetailView):
    model = Project
    template_name = 'joan/features_list.html'

class SprintView(generic.DetailView):
    model = Sprint
    template_name = 'joan/sprint.html'
