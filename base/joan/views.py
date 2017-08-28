from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Requirement, Feature, Ticket, Project, Release

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
    #context_object_name = 'latest_requirement_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProjectView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['requirement_list'] = Requirement.objects.filter(release__project__id__exact=self.kwargs['pk'])
        return context
