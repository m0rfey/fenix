"""fenix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns
from userprofile import api, views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #SignUp
    url(r'^signup/$', views.signup, name='signup'),

    #SignIn
    url(r'^signin/$', views.signin, name='signin'),

    #SignOut
    url(r'^signout/$', views.signout, name='signout'),

    # API
    url(r'^api-v1.0/users/$', api.UserList.as_view()),
    url(r'^api-v1.0/user/(?P<pk>[0-9]+)/$', api.UserDetail.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)
