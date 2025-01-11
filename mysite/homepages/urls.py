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
from django.contrib import admin
from django.urls import path

from .views import index, joinus, aboutus, studentsignup, signin, signout,  terms, credits, mission, ourstory, how
from django.views.generic import TemplateView

app_name = 'homepages'

urlpatterns = [
    path('', index, name='index'),
    path('joinus/', joinus, name='joinus'),
    path('aboutus', aboutus, name='aboutus'),
    path('signup', studentsignup, name='signup'),
    path('mission/', mission, name='mission'),
    path('ourstory/', ourstory, name='ourstory'),
    path('how/', how, name='how'),
    path('signin', signin, name='signin'),
    path('signout', signout, name='signout'),
    path('terms', terms, name='terms'),
    path('credits', credits, name='credits'),
    path('book', TemplateView.as_view(template_name="homepage/book.html"), name='book'),
    
]
