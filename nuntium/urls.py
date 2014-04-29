from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from .views import HomeTemplateView, MessageSearchView,\
    WriteItInstanceDetailView, \
    WriteItInstanceListView, \
    WriteItCreateInstanceView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeTemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^instances/create/?$', WriteItCreateInstanceView.as_view(), name='create_instance'),
    url(r'^instances/?$', WriteItInstanceListView.as_view(template_name='nuntium/template_list.html'), name='instance_list'),

    url(r'^search/?$', MessageSearchView(), name='search_messages'),
)
