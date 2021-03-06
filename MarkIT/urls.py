"""MarkIT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView, TemplateView
from django.views.static import serve as debug_serve

from MarkIT.views import ContactView
from students.views import students_list
from MarkIT.settings import MEDIA_ROOT, DEBUG


urlpatterns = [

    url( r'^$', students_list, name='home'),

    url( r'^students/', include('students.urls')),
    url( r'^groups/', include('groups.urls')),
    url( r'^journal/', include('journal.urls')),
    url( r'^exams/', include('exams.urls')),

    # contact form
    url(r'^contact/$', ContactView.as_view(), name='contact'),

    # User Related urls
    url( r'^users/profile/$', TemplateView.as_view(template_name='registration/profile.html'), name='profile'),
    url( r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    url( r'^register/complete/$', RedirectView.as_view(pattern_name='home'), name='registration_complete'),
    url( r'^users/', include('registration.backends.simple.urls', namespace='users')),

    # admin page
    url( r'^admin/', include(admin.site.urls)),

]

if DEBUG:
    # serve files from media folder
    urlpatterns += [
        url( r'^media/(?P<path>.*)$', debug_serve, {'document_root': MEDIA_ROOT})
    ]

