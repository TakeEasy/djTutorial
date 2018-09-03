# -*- coding:utf-8 -*-
# Author:YEAR

from django.urls import path,re_path
from crmAdmin import views

app_name='crmAdmin'

urlpatterns=[
    re_path(r'^$',views.Index.as_view(),name='table_index'),
    re_path(r'^(?P<appname>\w+)/(?P<tablename>\w+)$',views.DisplayTable.as_view(),name='table_display'),
    re_path(r'^(?P<appname>\w+)/(?P<tablename>\w+)/(?P<id>\w+)/change$',views.ChangeTable.as_view(),name='table_change'),
    re_path(r'^(?P<appname>\w+)/(?P<tablename>\w+)/(?P<id>\w+)/change/password$',views.ChangePassword.as_view(),name='table_changepwd'),
    re_path(r'^(?P<appname>\w+)/(?P<tablename>\w+)/add$',views.AddTable.as_view(),name='table_add'),
    re_path(r'^(?P<appname>\w+)/(?P<tablename>\w+)/(?P<id>\w+)/delete$',views.DeleteTable.as_view(),name='table_delete')
]

