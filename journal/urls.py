from django.conf.urls import include, url

from journal.views import JournalView

urlpatterns = [
    url( r'^(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),
]
