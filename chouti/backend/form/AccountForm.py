# -*- coding:utf-8 -*-
# Author:YEAR
from . import BaseFormField
from django import forms
from django.core.exceptions import ValidationError
import json

class RegisterForm(BaseFormField.BaseForm):
    def __init__(self):
        self.rgemail=BaseFormField.BaseContentFiled(required=True,error_dict={'required':'不能填空啊傻逼!'})
        self.rgcode = BaseFormField.BaseContentFiled(required=True, error_dict={'required': '不能填空啊傻逼!'})
        self.rgpwd = BaseFormField.BaseContentFiled(required=True, error_dict={'required': '不能填空啊傻逼!'})
        self.rgnick = BaseFormField.BaseContentFiled(required=True, error_dict={'required': '不能填空啊傻逼!'})
        self.rgsex = BaseFormField.BaseContentFiled(required=True, error_dict={'required': '不能填空啊傻逼!'})
        self.rgregion = BaseFormField.BaseContentFiled(required=True, error_dict={'required': '不能填空啊傻逼!'})
        self.rgsign = BaseFormField.BaseContentFiled(required=True, error_dict={'required': '不能填空啊傻逼!'})

class LoginForm(BaseFormField.BaseForm):
    def __init__(self):
        self.email=BaseFormField.BaseContentFiled(required=True,error_dict={'required':'不能填空啊傻逼!'})
        self.empwd = BaseFormField.BaseContentFiled(required=True, error_dict={'required': '不能填空啊傻逼!'})

class DjLoginForm(forms.Form):
    email=forms.EmailField(required=True,error_messages={"required":'不能填空啊傻逼!'})
    empwd=forms.CharField(required=True,error_messages={"required":'不能填空啊傻逼!'})

class SendCodeForm(forms.Form):
    em=forms.EmailField(error_messages={'invaild':'邮箱格式错误!!'})

class DjRegisterForm(forms.Form):
    rgemail=forms.CharField(required=True,error_messages={"required":'不能填空啊傻逼!!'})
    rgcode=forms.CharField(required=True,error_messages={"required":'不能填空啊傻逼!!'})
    rgpwd=forms.CharField(required=True,error_messages={"required":'不能填空啊傻逼!!'})
    rgnick=forms.CharField(required=True,error_messages={"required":'不能填空啊傻逼!!'})
    rgsex=forms.CharField(required=True,error_messages={"required":'不能填空啊傻逼!!'})
    rgregion=forms.CharField(required=True,error_messages={"required":'不能填空啊傻逼!!'})
    rgsign=forms.CharField(required=True,error_messages={"required":'不能填空啊傻逼!!'})

class JsonCustomerEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field,ValidationError):
            #return {'code':field.code,'message':field.message}
            return {'code': field.code, 'message': field.message}
        else:
            return json.JSONEncoder.default(self,field)