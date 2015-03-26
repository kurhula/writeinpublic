from django.conf.urls import patterns, url
# from django.conf.urls.i18n import i18n_patterns

from .views import WriteItInstanceDetailView, PerInstanceSearchView, \
    MessagesPerPersonView, MessageDetailView, MessagesFromPersonView

from django_downloadview import ObjectDownloadView
from nuntium.models import AnswerAttachment

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
download_attachment_view = ObjectDownloadView.as_view(model=AnswerAttachment, file_field="content")

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', WriteItInstanceDetailView.as_view(), name='instance_detail'),
    url(r'^(?P<instance_slug>[-\w]+)/messages/(?P<slug>[-\w]+)/$', MessageDetailView.as_view(), name='message_detail'),
    url(r'^(?P<slug>[-\w]+)/search/$', PerInstanceSearchView(), name='instance_search'),
    url(r'^(?P<slug>[-\w]+)/per_person/(?P<pk>[-\d]+)/$', MessagesPerPersonView.as_view(), name='messages_per_person'),
    url(r'^/attachment/(?P<pk>[-\d]+)/$', download_attachment_view, name='attachment'),
    url(r'^(?P<slug>[-\w]+)/from/(?P<message_slug>[-\w]+)/?$', MessagesFromPersonView.as_view(), name='all-messages-from-the-same-author-as'),
)
