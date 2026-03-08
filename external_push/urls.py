from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path

import external_push.views

app_name = "external_push"

# This gets added to the app's urlpatterns
# TODO - Convert this to be properly namespaced
external_push_urlpatterns = [
    ## External Push Views
    re_path(r'^push/$', external_push.views.external_push_list, name='external_push_list'),
    re_path(r'^push/add/$', external_push.views.external_push_generic_target_add, name='external_push_generic_target_add'),
    re_path(r'^push/view/(?P<push_target_id>[0-9]{1,20})/$', external_push.views.external_push_view, name='external_push_view'),
    re_path(r'^push/delete/(?P<push_target_id>[0-9]{1,20})/$', external_push.views.external_push_delete, name='external_push_delete'),

    re_path(r'^push/brewersfriend/add/$', external_push.views.external_push_brewers_friend_target_add, name='external_push_brewers_friend_target_add'),
    re_path(r'^push/brewersfriend/view/(?P<push_target_id>[0-9]{1,20})/$', external_push.views.external_push_brewers_friend_view, name='external_push_brewers_friend_view'),
    re_path(r'^push/brewersfriend/delete/(?P<push_target_id>[0-9]{1,20})/$', external_push.views.external_push_brewers_friend_delete, name='external_push_brewers_friend_delete'),

    re_path(r'^push/brewfather/add/$', external_push.views.external_push_brewfather_target_add, name='external_push_brewfather_target_add'),
    re_path(r'^push/brewfather/view/(?P<push_target_id>[0-9]{1,20})/$', external_push.views.external_push_brewfather_view, name='external_push_brewfather_view'),
    re_path(r'^push/brewfather/delete/(?P<push_target_id>[0-9]{1,20})/$', external_push.views.external_push_brewfather_delete, name='external_push_brewfather_delete'),

    re_path(r'^push/thingspeak/add/$', external_push.views.external_push_thingspeak_target_add, name='external_push_thingspeak_target_add'),
    re_path(r'^push/thingspeak/view/(?P<push_target_id>[0-9]{1,20})/$', external_push.views.external_push_thingspeak_view, name='external_push_thingspeak_view'),
    re_path(r'^push/thingspeak/delete/(?P<push_target_id>[0-9]{1,20})/$', external_push.views.external_push_thingspeak_delete, name='external_push_thingspeak_delete'),

    re_path(r'^push/grainfather/add/$', external_push.views.external_push_grainfather_target_add, name='external_push_grainfather_target_add'),
    re_path(r'^push/grainfather/view/(?P<push_target_id>[0-9]{1,20})/$', external_push.views.external_push_grainfather_view, name='external_push_grainfather_view'),
    re_path(r'^push/grainfather/delete/(?P<push_target_id>[0-9]{1,20})/$', external_push.views.external_push_grainfather_delete, name='external_push_grainfather_delete'),
]
