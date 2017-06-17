"""mason_philip_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
#from django.contrib.auth import views as auth_views

from story.views import home
from story.views import story
from pictures.views import pictures
from story.views import login_view, logout_view, specific
from story.views import post_new


urlpatterns = [

    url(r'^admin/', admin.site.urls),

    url(r'^story/(?P<blog_id>\d+)$', specific, name='specific'),
    url(r'^story/newpost/$', post_new, name='post_new'),
    url(r'^story/', story, name='story'),
    url(r'^pictures/', pictures, name='pictures'),

    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),

    url(r'^$', home, name='home'),
]
