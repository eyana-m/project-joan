from __future__ import unicode_literals

import datetime
import re
from django.utils import timezone
from django.utils.timezone import localtime, now
from django.db import models

DEFAULT_PROJECT = 1
DEFAULT_SPRINT = 1


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
    release_uat_start_date = models.DateField(blank=True, null=True)
    release_uat_end_date = models.DateField(blank=True, null=True)
    release_details = models.CharField(max_length=70,blank=True)

    def __str__(self):
        #return self.release_name
        return "Rel " + self.release_name

    def project_release(self):
        return self.project.project_name + " - Release " + self.release_name



# Items in the Business Requirements Document
class Requirement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=DEFAULT_PROJECT)
    reqd_id = models.CharField('No.',max_length=15,blank=True)
    requirement_heading = models.CharField('Category', max_length=70,blank=True)
    requirement_text = models.CharField('Requirement Name', max_length=300,unique=True)
    requirement_details = models.TextField('Details',max_length=400,blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    with_reqd_id = models.BooleanField('With Identifier',default=True)


    def __str__(self):
        return self.requirement_heading

    def reqd_id_heading(self):
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

    NEW = 'NW'
    DONE_USE_CASE = 'DU'
    IN_PROGRESS = 'IP'
    FOR_FV = 'FV'
    DONE = 'DO'
    FEATURE_STATUS_CHOICES = (
        (NEW, 'New'),
        (DONE_USE_CASE, 'UC Done'),
        (IN_PROGRESS, 'In Progress'),
        (FOR_FV, 'For FV'),
        (DONE, 'Done'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=DEFAULT_PROJECT)
    requirements = models.ManyToManyField(Requirement)
    release = models.ForeignKey(Release, on_delete=models.CASCADE, null=True, blank=True)
    feature_heading = models.CharField('Category', max_length=50,blank=True)
    feature_text = models.CharField('Feature Name', max_length=200,unique=True)
    feature_details = models.TextField('Details',max_length=300,blank=True,null=True)

    status = models.CharField(max_length=2,choices=FEATURE_STATUS_CHOICES,default=NEW,)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def is_new(self):
        return self.status in (self.NEW)

    def is_done(self):
        return self.status in (self.DONE)

    def __str__(self):
        return self.feature_text

    def save(self, *args, **kwargs):

        #Default Value for Release of null
        if not self.release:
            self.release= self.requirement.release

        super(Feature, self).save(*args, **kwargs)


### Sprint
### FK: Project, Release
### Has many tickets
class Sprint(models.Model):
    NEW = 'NW'
    ACTIVE = 'AC'
    DONE = 'DO'
    SPRINT_STATUS_CHOICES = (
        (NEW, 'New'),
        (ACTIVE, 'Active'),
        (DONE, 'Done'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=DEFAULT_PROJECT)
    release = models.ForeignKey(Release, on_delete=models.CASCADE, null=True, blank=True)
    sprint_name = models.CharField(max_length=20,blank=True)
    sprint_details = models.CharField(max_length=100,blank=True,null=True)
    sprint_start_date = models.DateField(blank=True, null=True)
    sprint_end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=2,choices=SPRINT_STATUS_CHOICES,default=NEW,)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return "%s - %s" %(self.release, self.sprint_name)

    @property
    def release_sprint(self):
        return "%s - %s" %(self.release, self.sprint_name)

    def save(self, *args, **kwargs):
        if self.sprint_end_date < localtime(now()).date():
            self.status = 'DO'
        elif self.sprint_start_date >localtime(now()).date():
            self.status = 'NW'
        elif self.sprint_end_date >= localtime(now()).date() and self.sprint_start_date <= localtime(now()).date():
            self.status = 'AC'
        else:
            self.status = 'NW'
        super(Sprint, self).save(*args, **kwargs)


# Filed feature or task tickets per sprint/iteration in the project management tool.
# One Feature can incur many tickets in many iteration
class Ticket(models.Model):

    NEW = 'NW'
    IN_PROGRESS = 'IP'
    FOR_FV = 'FV'
    DONE = 'DO'
    TICKET_STATUS_CHOICES = (
        (NEW, 'New'),
        (IN_PROGRESS, 'In Progress'),
        (FOR_FV, 'For FV'),
        (DONE, 'Done'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=DEFAULT_PROJECT)
    features = models.ManyToManyField(Feature)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, default=DEFAULT_SPRINT)
    ticket_id = models.CharField(max_length=10,blank=True)
    ticket_text = models.CharField(max_length=200)
    ticket_url = models.CharField(max_length=50,blank=True)
    dev_assigned = models.CharField(max_length=50,blank=True)
    status = models.CharField(max_length=2,choices=TICKET_STATUS_CHOICES,default=NEW,)
    is_feature = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.ticket_text

    def is_new(self):
        return self.status in (self.NEW)

    def is_done(self):
        return self.status in (self.DONE)

    def is_np(self):
        return self.status in (self.IN_PROGRESS)

    def is_fv(self):
        return self.status in (self.FOR_FV)


    class Meta:
        ordering = ['sprint', 'id', 'ticket_text']



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
