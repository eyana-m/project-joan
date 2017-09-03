from django.conf.urls import url

from . import views

app_name = 'joan'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^project/(?P<pk>[a-zA-Z0-9-]+)/$', views.ProjectView.as_view(), name='project'),
    url(r'^requirement/(?P<pk>[a-zA-Z0-9-]+)/$', views.RequirementView.as_view(), name='requirement'),
    url(r'^feature/(?P<pk>[a-zA-Z0-9-]+)/$', views.FeatureView.as_view(), name='feature'),
    url(r'^release/(?P<pk>[a-zA-Z0-9-]+)/$', views.ReleaseView.as_view(), name='release'),
    url(r'^project/(?P<pk>[a-zA-Z0-9-]+)/requirements', views.ProjectRequirementsView.as_view(), name='requirements_list'),
]
