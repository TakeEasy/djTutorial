# -*- coding:utf-8 -*-
# Author:YEAR
from django.urls import path,re_path
from . import views
app_name='chouti'
urlpatterns=[
    path('',views.index,name='index'),
    path('send_code/',views.SendCodeHandler.as_view(),name='sendCode'),
    path('login/',views.LoginHandler.as_view(),name='login'),
    path('register/',views.RegisterHandler.as_view(),name='register'),
    path('urltitle/',views.urlTitleHandler.as_view(),name='urltitle'),
    path('publish/',views.publishHandler.as_view(),name='publish'),
    path('dianzan/',views.dianzanHandler.as_view(),name='dianzan'),
    path('getcomments/',views.commentsHandler.as_view(),name='getcomments'),
    path('huifu/',views.huifuHandler.as_view(),name='huifu'),
    path('djtestform/',views.djangoFormTest.as_view(),name='djformtest'),
    path('djtestmodelform/',views.djangoModelFormTest.as_view(),name='djmodelformtest'),
    re_path(r'edit-djtestmodelform-(?P<nid>\d+)/',views.EditdjangoModelFormTest.as_view(),name='editdjmodelformtest'),
    path('cacheTest/',views.cacheTest.as_view(),name='cacheTest'),
    path('bootstrapTest/',views.bootstrapTest.as_view(),name='bootstrapTest')
]