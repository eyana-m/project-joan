# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.utils import timezone
from django.db import models

# Items in the Business Requirements Document
class Requirement(models.Model):
    reqd_id = models.CharField(max_length=10,blank=True)
    requirement_heading = models.CharField(max_length=50,blank=True)
    requirement_text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)


    def __str__(self):
        return self.reqd_id + " " + self.requirement_heading

    class Meta:
        ordering = ['reqd_id', 'id']

# Also known as Use Cases. Feature sounds more abstract.
class Feature(models.Model):
    requirement = models.ManyToManyField(Requirement)
    feature_heading = models.CharField(max_length=50,blank=True)
    feature_text = models.TextField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)


    def __str__(self):
        return self.feature_text

# Filed feature or task tickets per sprint/iteration in the project management tool.
# One Feature can incur many tickets in many iteration
class Ticket(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    ticket_id = models.CharField(max_length=10,blank=True)
    ticket_text = models.CharField(max_length=200)
    release = models.CharField(max_length=5)
    iteration = models.CharField(max_length=5)
    is_feature = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)


    def __str__(self):
        return self.ticket_text
