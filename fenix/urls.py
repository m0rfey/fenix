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
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework.urlpatterns import format_suffix_patterns

from fenix import settings
from userprofile import api, views
from catalog.views import index, category, view_details, expres_save, search_key, view_expresfile, download_link, \
    download_d, myfiles, addfile, get_addfile, search

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # Home
    url(r'^$', index, name='home'),

    # SignUp
    url(r'^signup/$', views.signup, name='signup'),

    # SignIn
    url(r'^signin/$', views.signin, name='signin'),

    # SignOut
    url(r'^signout/$', views.signout, name='signout'),

    # Profile
    url(r'^user-(?P<user_id>\d+)/$', views.profile, name='user_profile'),
    url(r'^user-(?P<user_id>\d+)/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^user-(?P<user_id>\d+)/edit/save/$', views.edit_profile, name='edit_profile_save'),
    url(r'^user-(?P<user_id>\d+)/myfiles/$', myfiles, name='myfiles'),
    url(r'addfiles/$', addfile, name='addfiles'),
    url(r'^addfiles/add$', get_addfile, name='add'),

    # Details
    url(r'^view-(?P<slug>[\w-]+)/$', view_details, name='details'),
    url(r'^view-(?P<slug>[\w-]+)/download/(?P<file_id>\d+)/$', download_d, name='download_d' ),

    #
    url(r'^addfile/new/$', expres_save, name='addfile'),
    #
    url(r'^search-key/$', search_key, name='search_key' ),
    url(r'^get-(?P<slug>[\w-]+)/$', view_expresfile, name='search_Link' ),
    url(r'^get-(?P<slug>[\w-]+)/download/(?P<file_id>\d+)/$', download_link, name='download' ),

    url(r'^search/$', search, name='search'),



    # Category
    url(r'^views-(?P<category_slug>[\w-]+)/', category, name='category'),


    # API
    url(r'^api-v1.0/users/$', api.UserList.as_view()),
    url(r'^api-v1.0/user/(?P<pk>[0-9]+)/$', api.UserDetail.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
