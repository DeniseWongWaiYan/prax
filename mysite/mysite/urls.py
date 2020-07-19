"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings 
from django.utils.translation import gettext_lazy as _

#
urlpatterns =[
#    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('home/', include('homepages.urls')),
    path('courses/', include('courses.urls')),
    path('studentmembership/', include('studentmemberships.urls')),
    path('tutors/', include('tutors.urls')),
    path('parents/', include('parents.urls')),
    path('grades/', include('grades.urls')),
    path('vocab/', include('vocab.urls')),
    path('messages/', include('postman.urls')), prefix_default_language=True)
#
#
#urlpatterns = i18n_patterns(
#    path(_('home'), include('homepages.urls')),
#    path(_('courses/'), include('courses.urls')),
#    path(_('studentmembership/'), include('studentmemberships.urls')),
#    path(_('tutors/'), include('tutors.urls')),
#    path(_('parents/'), include('parents.urls')),
#    path(_('grades/'), include('grades.urls')),
#    path(_('vocab/'), include('vocab.urls')),
#    path(_('messages/'), include('postman.urls')),
#)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

