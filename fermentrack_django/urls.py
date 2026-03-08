from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path

import app.views
import app.profile_views
import app.setup_views
import app.beer_views
import app.api.lcd
import app.api.clog
import app.api.devices

import firmware_flash.urls
import gravity.urls
import external_push.urls

admin.autodiscover()

# In addition to urlpatterns below, three paths are mapped by the nginx config file:
# r'^static/' - Maps to collected_static/. Contains collected static files.
# r'^media/' - Maps to media/. Contains uploaded files. Currently unused.
# r'^data/' - Maps to data/. Contains data points collected by brewpi.py.

# Separately, all r'^firmware/' urls are contained in firmware_flash/urls.py

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', app.views.siteroot, name='siteroot'),

    re_path(r'^upgrade/$', app.views.github_trigger_upgrade, name='github_trigger_upgrade'),
    # url(r'^upgrade/force/$', app.views.github_trigger_force_upgrade, name='github_trigger_force_upgrade'),
    # url(r'^upgrade/delete_lock/$', app.views.delete_upgrade_lock_file, name='delete_upgrade_lock_file'),

    ### Device Views
    re_path(r'^devices/$', app.views.device_lcd_list, name='device_lcd_list'),
    re_path(r'^devices/add/$', app.views.add_device, name='device_add'),

    ## New install Guided Setup Views
    re_path(r'^setup/$', app.setup_views.setup_splash, name="setup_splash"),
    re_path(r'^setup/add_user/$', app.setup_views.setup_add_user, name="setup_add_user"),
    re_path(r'^setup/settings/$', app.setup_views.setup_config, name="setup_config"),  # This is settings.CONSTANCE_SETUP_URL

    ## Device Guided Setup Views
    re_path(r'^devices/guided/$', app.setup_views.device_guided_select_device, name='device_guided_select_device'),
    re_path(r'^devices/guided/(?P<device_family>[A-Za-z0-9]{1,20})/flash_prompt/$', app.setup_views.device_guided_flash_prompt, name='device_guided_flash_prompt'),
    re_path(r'^devices/guided/(?P<device_family>[A-Za-z0-9]{1,20})/flash/$', app.setup_views.device_guided_flash_prompt, name='device_guided_flash_prompt'),
    re_path(r'^devices/guided/(?P<device_family>[A-Za-z0-9]{1,20})/connection/$', app.setup_views.device_guided_serial_wifi, name='device_guided_serial_wifi'),
    re_path(r'^devices/guided/mdns/$', app.setup_views.device_guided_find_mdns, name='device_guided_mdns'),
    re_path(r'^devices/guided/mdns/(?P<mdns_id>[A-Za-z0-9.]{1,60})/$', app.setup_views.device_guided_add_mdns, name='device_guided_add_mdns'),
    re_path(r'^devices/guided/serial/autodetect/(?P<device_family>[A-Za-z0-9]{1,20})/$', app.setup_views.device_guided_serial_autodetect, name='device_guided_serial_autodetect'),

    ## Other main device views
    re_path(r'^devices/(?P<device_id>\d{1,20})/control_constants/$', app.views.device_control_constants, name='device_control_constants'),
    re_path(r'^devices/(?P<device_id>\d{1,20})/dashboard/$', app.views.device_dashboard, name='device_dashboard'),
    re_path(r'^devices/(?P<device_id>\d{1,20})/dashboard/beer/(?P<beer_id>\d{1,20})/$', app.views.device_dashboard, name='device_dashboard_beer'),
    re_path(r'^devices/(?P<device_id>\d{1,20})/dashboard/beer/(?P<beer_id>\d{1,20})/annotations.json$', app.views.almost_json_view, name='almost_json_view'),
    # TODO - Implement backlight toggle AJAX API call
    re_path(r'^devices/(?P<device_id>\d{1,20})/backlight/toggle/$', app.views.device_dashboard, name='device_toggle_backlight'),
    # TODO - Implement temperature control AJAX API calls
    re_path(r'^devices/(?P<device_id>\d{1,20})/temp_control/$', app.views.device_temp_control, name='device_temp_control'),
    re_path(r'^devices/(?P<device_id>\d{1,20})/reset/$', app.views.device_eeprom_reset, name='device_eeprom_reset'),
    re_path(r'^devices/(?P<device_id>\d{1,20})/wifi_reset/$', app.views.device_wifi_reset, name='device_wifi_reset'),
    re_path(r'^devices/(?P<device_id>\d{1,20})/restart/$', app.views.device_restart, name='device_restart'),
    re_path(r'^devices/(?P<device_id>\d{1,20})/manage/$', app.views.device_manage, name='device_manage'),
    re_path(r'^devices/(?P<device_id>\d{1,20})/extended_settings/$', app.views.device_extended_settings, name='device_extended_settings'),
    re_path(r'^devices/(?P<device_id>\d{1,20})/uninstall/$', app.views.device_uninstall, name='device_uninstall'),

    # Device Utility & Internal Views
    re_path(r'^devices/(?P<device_id>\d{1,20})/beer/create/$', app.beer_views.beer_create, name='beer_create'),
    re_path(r'^devices/(?P<device_id>\d{1,20})/beer/status/(?P<logging_status>[A-Za-z0-9]{1,20})/$', app.beer_views.beer_logging_status, name='beer_logging_status'),

    re_path(r'^devices/(?P<device_id>\d{1,20})/sensors/$', app.views.sensor_list, name='sensor_list'),
    re_path(r'^devices/(?P<device_id>\d{1,20})/sensors/config/$', app.views.sensor_config, name='sensor_config'),
    re_path(r'^devices/(?P<device_id>\d{1,20})/sensors/refresh/$', app.views.sensor_refresh, name='sensor_refresh'),

    re_path(r'^devices/(?P<device_id>\d{1,20})/debug_connection/$', app.views.debug_connection, name='device_debug_connection'),


    # Fermentation Profile Views
    re_path(r'^fermentation_profile/list/$', app.profile_views.profile_list, name='profile_list'),
    re_path(r'^fermentation_profile/new/$', app.profile_views.profile_new, name='profile_new'),
    re_path(r'^fermentation_profile/import/$', app.profile_views.profile_import, name='profile_import'),
    re_path(r'^fermentation_profile/(?P<profile_id>\d{1,20})/$', app.profile_views.profile_new, name='profile_view'),
    re_path(r'^fermentation_profile/(?P<profile_id>\d{1,20})/edit/$', app.profile_views.profile_edit, name='profile_edit'),
    re_path(r'^fermentation_profile/(?P<profile_id>\d{1,20})/delete/$', app.profile_views.profile_delete, name='profile_delete'),
    re_path(r'^fermentation_profile/(?P<profile_id>\d{1,20})/undelete/$', app.profile_views.profile_undelete, name='profile_undelete'),
    re_path(r'^fermentation_profile/(?P<profile_id>\d{1,20})/point/(?P<point_id>\d{1,20})/delete$', app.profile_views.profile_setpoint_delete, name='profile_setpoint_delete'),
    re_path(r'^fermentation_profile/(?P<profile_id>\d{1,20})/csv/$', app.profile_views.profile_points_to_csv, name='profile_points_to_csv'),
    re_path(r'^fermentation_profile/(?P<profile_id>\d{1,20})/copy/$', app.profile_views.profile_copy, name='profile_copy'),
    re_path(r'^fermentation_profile/(?P<profile_id>\d{1,20})/rename/$', app.profile_views.profile_rename, name='profile_rename'),
    re_path(r'^fermentation_profile/(?P<profile_id>\d{1,20})/notes/$', app.profile_views.profile_notes, name='profile_notes'),

    # Beer Views
    re_path(r'^beer/list/$', app.beer_views.beer_list, name='beer_list'),
    re_path(r'^beer/(?P<beer_id>\d{1,20})/delete/$', app.beer_views.beer_delete, name='beer_delete'),

    # Api Views
    re_path(r'^api/lcd/(?P<device_id>\d{1,20})/$', app.api.lcd.getLCD, name="getLCD"),  # For a single device
    re_path(r'^api/lcd/$', app.api.lcd.getLCDs, name="getLCDs"),  # For all devices/LCDs
    re_path(r'^api/panel/(?P<device_id>\d{1,20})/$', app.api.lcd.getPanel, name="getPanel"),  # For a single device
    # Read controller log files
    # for the /api/log endpoint, converting to /api/log/<returntype>/<devicetype>/<logtype>/d<device_id>/l<lines>/
    re_path(r'^api/log/(?P<return_type>text|json)/(?P<device_type>\w{1,20})/(?P<logfile>stdout|stderr)/d(?P<device_id>\d{1,20})/$', app.api.clog.get_device_log_combined, name="get_device_log"),
    re_path(r'^api/log/(?P<return_type>text|json)/(?P<device_type>\w{1,20})/(?P<logfile>stdout|stderr)/d(?P<device_id>\d{1,20})/l(?P<lines>\d{1,20})/$', app.api.clog.get_device_log_combined, name="get_device_log_lines"),
    re_path(r'^api/log/(?P<return_type>text|json)/(?P<device_type>\w{1,20})/(?P<logfile>stdout|stderr)/$', app.api.clog.get_device_log_combined, name="get_app_log"),
    re_path(r'^api/log/(?P<return_type>text|json)/(?P<device_type>\w{1,20})/(?P<logfile>stdout|stderr)/l(?P<lines>\d{1,20})/$', app.api.clog.get_device_log_combined, name="get_app_log_lines"),
    # api/gravity views are located in the gravity app

    # These API endpoints are used by the BrewPi Script Caller
    re_path(r'^api/devices/$', app.api.devices.get_devices, name="getDevices"),  # To retrieve a BrewPiDevice
    re_path(r'^api/save_point/$', app.api.devices.create_beer_log_point, name="savePoint"),  # To create a BeerLogPoint

    # Login/Logout Views
    re_path(r'^accounts/login/$', app.views.login, name='login'),  # This is also settings.LOGIN_URL
    re_path(r'^accounts/logout/$', app.views.logout, name='logout'),

    # Site-specific views (Help, Settings, etc.)
    re_path(r'site/settings/$', app.views.site_settings, name="site_settings"),
    re_path(r'site/help/$', app.views.site_help, name="site_help"),

    path("backups/", include("backups.urls", namespace="backups")),

] + static(settings.DATA_URL, document_root=settings.DATA_ROOT) + \
              firmware_flash.urls.firmware_flash_urlpatterns + gravity.urls.gravity_urlpatterns + \
              external_push.urls.external_push_urlpatterns
# TODO - Convert the above to be properly namespaced
