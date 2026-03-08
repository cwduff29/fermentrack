from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path

import gravity.views
import gravity.views_ispindel
import gravity.views_tilt
import gravity.api.sensors

app_name = "gravity"

# This gets added to the app's urlpatterns
gravity_urlpatterns = [
    ## Device Guided Setup Views
    re_path(r'^gravity/$', gravity.views.gravity_list, name='gravity_list'),
    re_path(r'^gravity/add/$', gravity.views.gravity_add_board, name='gravity_add_board'),
    re_path(r'^gravity/manual_point/(?P<manual_sensor_id>[A-Za-z0-9]{1,20})/$', gravity.views.gravity_add_point, name='gravity_add_point'),
    # url(r'^gravity/add/tilt/$', firmware_flash.views.firmware_refresh_list, name='firmware_flash_refresh_list'),
    # url(r'^gravity/add/tilt/$', firmware_flash.views.firmware_refresh_list, name='firmware_flash_refresh_list'),

    # Sensor Views
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/$', gravity.views.gravity_dashboard, name='gravity_dashboard'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/log/(?P<log_id>[A-Za-z0-9]{1,20})/view/$', gravity.views.gravity_dashboard, name='gravity_dashboard_log'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/attach/$', gravity.views.gravity_attach, name='gravity_attach'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/detach/$', gravity.views.gravity_detach, name='gravity_detach'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/uninstall/$', gravity.views.gravity_uninstall, name='gravity_uninstall'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/manage/$', gravity.views.gravity_manage, name='gravity_manage'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/log/(?P<log_id>[A-Za-z0-9]{1,20})/annotations.json$', gravity.views.almost_json_view, name='gravity_almost_json_view'),

    # Sensor Log Views
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/log/create/$', gravity.views.gravity_log_create, name='gravity_log_create'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/log/stop/$', gravity.views.gravity_log_stop, name='gravity_log_stop'),

    # Log Management
    re_path(r'^gravity/logs/$', gravity.views.gravity_log_list, name='gravity_log_list'),
    re_path(r'^gravity/logs/(?P<log_id>\d{1,20})/delete/$', gravity.views.gravity_log_delete, name='gravity_log_delete'),

    # API Calls
    re_path(r'^api/gravity/(?P<device_id>\d{1,20})/$', gravity.api.sensors.get_gravity_sensors, name="getSensor"),  # For a single device
    re_path(r'^api/gravity/$', gravity.api.sensors.get_gravity_sensors, name="getSensors"),  # For all sensors
    re_path(r'^api/gravity/ispindel/(?P<device_id>\d{1,20})/$', gravity.api.sensors.get_ispindel_extras, name="get_ispindel_extras"),  # Specific to iSpindel devices, allows for easy calibration
    re_path(r'^api/gravity/tilt/(?P<device_id>\d{1,20})/$', gravity.api.sensors.get_tilt_extras, name="get_tilt_extras"),  # Specific to Tilt Hydrometers, allows for easy calibration

    # iSpindel specific Views
    re_path(r'^i[sS]{1}pind[el]{2}/?$', gravity.views_ispindel.ispindel_handler, name="gravity_ispindel"),  # Handler for ispindel gravity readings
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/ispindel/setup/$', gravity.views_ispindel.gravity_ispindel_setup, name='gravity_ispindel_setup'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/ispindel/coefficients/$', gravity.views_ispindel.gravity_ispindel_coefficients, name='gravity_ispindel_coefficients'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/ispindel/calibration/add/$', gravity.views_ispindel.gravity_ispindel_add_calibration_point, name='gravity_ispindel_add_calibration_point'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/ispindel/calibration/delete/(?P<point_id>[A-Za-z0-9]{1,20})/$', gravity.views_ispindel.gravity_ispindel_delete_calibration_point, name='gravity_ispindel_delete_calibration_point'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/ispindel/calibration/calibrate/$', gravity.views_ispindel.gravity_ispindel_calibrate, name='gravity_ispindel_calibrate'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/ispindel/calibration/guided/(?P<step>[A-Za-z0-9]{1,20})$', gravity.views_ispindel.gravity_ispindel_guided_calibration, name='gravity_ispindel_guided_calibration'),

    # Tilt specific Views
    re_path(r'^[tT]{1}ilt[bB]{1}ridge/?$', gravity.views_tilt.tiltbridge_handler, name="gravity_tiltbridge"), # Handler for tiltbridge gravity readings
    # url(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/tilt/setup/$', gravity.views_tilt.gravity_tilt_setup, name='gravity_tilt_setup'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/tilt/coefficients/gravity/$', gravity.views_tilt.gravity_tilt_coefficients, name='gravity_tilt_coefficients'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/tilt/calibration/gravity/add/$', gravity.views_tilt.gravity_tilt_add_gravity_calibration_point, name='gravity_tilt_add_gravity_calibration_point'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/tilt/calibration/gravity/delete/(?P<point_id>[A-Za-z0-9]{1,20})/$', gravity.views_tilt.gravity_tilt_delete_gravity_calibration_point, name='gravity_tilt_delete_gravity_calibration_point'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/tilt/calibration/gravity/calibrate/$', gravity.views_tilt.gravity_tilt_calibrate, name='gravity_tilt_calibrate'),
    re_path(r'^gravity/sensor/(?P<sensor_id>[A-Za-z0-9]{1,20})/tilt/calibration/gravity/guided/(?P<step>[A-Za-z0-9]{1,20})$', gravity.views_tilt.gravity_tilt_guided_calibration, name='gravity_tilt_guided_calibration'),

    # TiltBridge specific views
    re_path(r'^gravity/tiltbridge/add/$', gravity.views_tilt.gravity_tiltbridge_add, name='gravity_tiltbridge_add'),
    re_path(r'^gravity/tiltbridge/update/(?P<tiltbridge_id>[A-Za-z0-9]{1,20})/set_url/$', gravity.views_tilt.gravity_tiltbridge_set_url, name='gravity_tiltbridge_set_url'),
    re_path(r'^gravity/tiltbridge/update/(?P<tiltbridge_id>[A-Za-z0-9]{1,20})/set_url/(?P<sensor_id>[A-Za-z0-9]{1,20})$', gravity.views_tilt.gravity_tiltbridge_set_url, name='gravity_tiltbridge_set_url'),
    re_path(r'^gravity/tiltbridge/urlerror/(?P<tiltbridge_id>[A-Za-z0-9]+)/$', gravity.views_tilt.gravity_tiltbridge_urlerror, name='gravity_tiltbridge_urlerror'),

]
