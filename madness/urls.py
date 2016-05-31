"""
Copyright 2016, Paul Powell, All rights reserved.
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from tournament.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page':'/'}),
    url(r'^accounts/register/$', RegisterView.as_view(success_url="/accounts/login"), name='register'),
    url(r'^$', home_page, name='home-page'),
    url(r'^tournament/generate/$', run_tournament, name='run-tournament'),
    url(r'^tournament/generate/(?P<option_id>[0-9]+)/$', run_tournament_options, name='run-tournament-options'),
    url(r'^tournament/options/$', create_with_options, name='create-with-options'),
    url(r'^tournament/(?P<result_id>[0-9]+)/$', view_result, name='view-result'),
    url(r'^tournament/(?P<result_id>[0-9]+)/save$', save_result, name='save-result'),
    url(r'^tournament/(?P<result_id>[0-9]+)/remove$', remove_result, name='remove-result'),
    url(r'^tournament/(?P<result_id>[0-9]+)/full$', view_full_result, name='view-full-result'),
    url(r'^tournament/brackets', my_brackets, name='my-brackets'),
    url(r'^tournament/help/introduction', help_introduction, name='help-introduction'),
    url(r'^tournament/help/create', help_create, name='help-create'),
    url(r'^tournament/help/save', help_save, name='help-save'),
    url(r'^tournament/help/show', help_show, name='help-show'),
]
