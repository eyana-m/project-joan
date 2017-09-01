from __future__ import unicode_literals

import datetime
import re
from django.utils import timezone
from django.db import models

DEFAULT_PROJECT = 1


class Project (models.Model):
    project_name = models.CharField(max_length=50,unique = True)
    slug = models.SlugField(max_length=10, null=True,unique=True)
    project_company = models.CharField(max_length=50)
    project_description = models.CharField(max_length=50)
    project_start_date = models.DateField(blank=True,null=True)
    project_end_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.project_name


class Release (models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=DEFAULT_PROJECT)
    release_name = models.CharField(max_length=50)
    release_target_date = models.DateField(blank=True, null=True)
    release_actual_date = models.DateField(blank=True, null=True)
    release_details = models.CharField(max_length=70,blank=True)

    def __str__(self):
        #return self.release_name
        return "Release " + self.release_name

    def project_release(self):
        return self.project.project_name + " - Release " + self.release_name


# Items in the Business Requirements Document
class Requirement(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE, null=True, blank=True)
    reqd_id = models.CharField(max_length=15,blank=True)
    requirement_heading = models.CharField(max_length=70,blank=True)
    requirement_text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)


    def __str__(self):
        return self.reqd_id + " " + self.requirement_heading

    class Meta:
        ordering = ['reqd_id', 'id']

    def save(self, *args, **kwargs):

        #Default Value for Requirement ID if null
        if not self.reqd_id:
            self.reqd_id = self.requirement_text.split(None, 1)[0] + "."

        #Default Value for Requirement Heading if null
        if not self.requirement_heading:
            self.requirement_heading = self.requirement_text.splitlines()[0].split(None, 1)[1]

        super(Requirement, self).save(*args, **kwargs)


# Also known as Use Cases. Feature sounds more abstract.
class Feature(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=DEFAULT_PROJECT)
    requirement = models.ManyToManyField(Requirement)
    release = models.ForeignKey(Release, on_delete=models.CASCADE, null=True, blank=True)
    feature_heading = models.CharField('Category', max_length=50,blank=True)
    feature_text = models.CharField('Feature Name', max_length=200)
    feature_detail = models.TextField('Details',max_length=300,blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)


    def __str__(self):
        return self.feature_text

# Filed feature or task tickets per sprint/iteration in the project management tool.
# One Feature can incur many tickets in many iteration
class Ticket(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=DEFAULT_PROJECT)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    ticket_id = models.CharField(max_length=10,blank=True)
    ticket_text = models.CharField(max_length=200)
    ticket_url = models.CharField(max_length=50,blank=True)
    release = models.ForeignKey(Release, on_delete=models.CASCADE, null=True, blank=True)
    #release = models.CharField(max_length=5)
    iteration = models.CharField(max_length=5,null=True, blank=True)
    is_feature = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.ticket_text

    def release_sprint(self):
        return "Rel %s - Iter %s" %(self.release, self.iteration)

    class Meta:
        ordering = ['release', 'id', 'ticket_text']


# Relate to Requirements, Meeting
# Can add file attachment, screenshots for proof
class Agreement(models.Model):
    requirement = models.ManyToManyField(Requirement)
    agmt_date_raised = models.DateTimeField(blank=True)
    agmt_date_resolved = models.DateTimeField(blank=True)
    agmt_issue = models.CharField(max_length=100)
    agmt_issue_details = models.TextField(blank=True)
    agmt_answer = models.CharField(max_length=100)
    agmt_answer_details = models.TextField(blank=True)
    agmt_resource_person = models.CharField(max_length=50)
    agmt_medium = models.CharField(max_length=50)
    is_external = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)


    def __str__(self):
        return self.agmt_issue

    class Meta:
        ordering = ['agmt_date_raised', 'id', 'agmt_issue']
