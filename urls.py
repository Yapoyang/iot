"""iot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from post.views import recv_data,show
from control.views import load_data,last
from iot_test.views import contact,load_test,show_test,find,pr,sensor_location,medical_load,medical_record_post,medical_record_find,light_adjust_vlc,dropsys
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^post/$',recv_data),
    url(r'^show/$',show),
    url(r'^last/$',last),
    url(r'^load/$',load_data),
    url(r'^contact/$',contact),
    url(r'^turnlight/$',load_test),
    url(r'^showdata',show_test),
    url(r'^findmachine',find),
    url(r'^pr',pr),
    url(r'^sensor_location',sensor_location),
    url(r'^medical_load',medical_load),
    url(r'^medical_record_post/(?P<value>\w+)/$',medical_record_post),
    url(r'^medical_record_find',medical_record_find),
    url(r'^vlc_v13_lightcontrol',light_adjust_vlc),
    url(r'^dropsys',dropsys),
    #url(r'^light/$',light_test),
]
