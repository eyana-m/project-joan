from django.conf.urls import url

from . import views

app_name = 'joan'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[a-zA-Z0-9-]+)/$', views.ProjectView.as_view(), name='project'),
]
