# -*- coding:utf-8 -*-
# Author:YEAR
from django.urls import path,re_path
from . import views
app_name='myCRM'
urlpatterns=[
    path('',views.Index,name='Index'),
    path('account/login/',views.AccountLogin.as_view(),name='account_login'),
    path('account/logout/',views.AccountLogout.as_view(),name='account_logout'),
    path('salesIndex',views.Index,name='sales_index'),
    path('studentIndex',views.Index,name='student_index'),
    path('teacherIndex',views.Index,name='teacher_index'),
    path('customerList',views.CustomerList,name='customer_list'),
    re_path(r'customer/(?P<id>\w+)/enroll',views.Enroll,name='customer_enroll')
]