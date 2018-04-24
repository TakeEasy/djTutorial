# -*- coding:utf-8 -*-
# Author:YEAR

from django.urls import path
from . import views

app_name='school'
urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.Login.as_view(),name='login'),
    path('logout/',views.logout,name='logout'),
    path('classadmin/',views.classadmin,name='classadmin'),
    path('teacheradmin/',views.teacheradmin,name='teacheradmin'),
    path('studentadmin/',views.studentadmin,name='studentadmin')
]