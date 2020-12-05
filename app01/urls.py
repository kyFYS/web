from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from app01.views import account,home

urlpatterns = [
    url(r'^send/sms/$', account.send_sms,name='send_sms'),
    url(r'^register/$', account.register, name='register'),
    url(r'^login_sms/$', account.login_sms, name='login_sms'),
    url(r'^login/$', account.login, name='login'),
    url(r'^image/code/$', account.image_code, name='image_code'),
    url(r'^index/$', home.index, name='index'),
    url(r'^logout/$', account.logout, name='logout'),
]