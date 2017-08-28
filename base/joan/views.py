from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Requirement, Feature, Ticket, Project


class IndexView(generic.ListView):
    template_name = 'joan/index.html'
    context_object_name = 'latest_project_list'

    def get_queryset(self):
        return Project.objects.order_by('id')[:10]

class DetailView(generic.DetailView):
    model = Requirement
    template_name = 'joan/detail.html'
