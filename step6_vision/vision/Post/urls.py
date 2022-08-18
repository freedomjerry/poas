
from django.contrib import admin
from django.urls import path
from django import urls
from django.conf.urls import url
from Post import views
app_name = 'Post'   # 这里是为了url反向解析用

urlpatterns = [
    #url(r'^$', views.index, name="index"),
    url(r'^$', views.index, name="index"),
    url(r'^main/', views.receive_data),
    url(r'^example_virus/', views.examlpe_virus, name="example_virus"),
    url(r'^example_fire/', views.examlpe_fire, name="example_fire"),
    url(r'^example_earthquake/', views.examlpe_earthquake, name="example_earthquake"),
    url(r'^example_sample/', views.examlpe_sample, name="example_sample"),

]