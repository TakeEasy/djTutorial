# -*- coding:utf-8 -*-
# Author:YEAR
from myCRM import models
from django.shortcuts import render


enabled_admin={}

class BaseAdmin(object):
    list_display=[]
    list_filter=[]
    search_fields=[]
    list_per_page=5
    list_horizontal=[]
    actions=[]
    readonly_fields=[]
    exclude_fields=[]
    action_buttons=[]
    readonly_table=False
    ordering=None
    model=None

    def delete_selected_objs(self,request,querysets):
        print('delete_selected_obj',request,querysets)
        render(request, 'crmAdmin/table_delete.html',
               {'adminClass': self, 'dataObj': querysets, 'appname': self.model._meta.app_label, 'tablename': self.model._meta.model_name})

    def custom_form_validation(self,error_list):
        print('custom_form_validation')
        return error_list

class CustomerAdmin(BaseAdmin):
    list_display=['qq','name','wechat','source','consult_course','date']
    list_filter = ['source','consultant','consult_course','date']
    search_fields = ['qq','name','wechat']
    list_horizontal = ['tags',]
    readonly_fields=['qq',]
    actions = ['delete_selected_objs',]
    action_buttons=['enroll',]
    ordering = 'id'

class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ['customer','consultant','intention','date']
    list_filter = ['intention','date']
    search_fields = ['customer__qq','consultant__name']
    ordering = '-id'

class UserProfileAdmin(BaseAdmin):
    list_display = ['email','name','roles']
    list_filter = ['roles']
    search_fields = ['email','name']
    readonly_fields = ['password']
    list_horizontal = ['roles','groups','user_permissions']
    exclude_fields = ['last_login',]


def register(model_class,admin_class=None):
    if model_class._meta.app_label not in enabled_admin:
        enabled_admin[model_class._meta.app_label]={}

    admin_class.model = model_class
    enabled_admin[model_class._meta.app_label][model_class._meta.model_name]=admin_class

register(models.Customer,CustomerAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)
register(models.UserProfile,UserProfileAdmin)
