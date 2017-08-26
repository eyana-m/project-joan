from __future__ import unicode_literals

from django.contrib import admin

from .models import Requirement

from .models import Feature

from .models import Ticket

# class ChildInline(admin.TabularInline):
#     model = Feature
#
# class ParentAdmin(admin.ModelAdmin):
#     inlines = [
#         ChildInline,
#     ]
#
#
# admin.site.register(Feature)
admin.site.register(Requirement)
admin.site.register(Feature)
admin.site.register(Ticket)
