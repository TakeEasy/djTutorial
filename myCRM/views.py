from django.shortcuts import render,reverse,Http404
from django.http import HttpResponse,HttpResponseRedirect
from . import models
from django import views
import json
from django.utils.decorators import method_decorator
from chouti.backend import common
from chouti.backend.utils import message
from chouti.backend.utils import url
from chouti.backend.form import AccountForm
from chouti.backend.form import DjangoTestForm
import datetime
from django.utils.timezone import localtime
import os
import re
from urllib import request as urlrequest
from django.db.models import F,Q
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from myCRM.forms import SalesForms

# @login_required
# class Index(views.View):
#     def get(self,request,*args,**kwargs):
#         return HttpResponse(render(request,'myCRM/index.html'))
#     def post(self,request,*args,**kwargs):
#         pass
@login_required
def Index(request):
    return HttpResponse(render(request,'myCRM/index.html'))

def Enroll(request,id):
    message={}
    msg="http://localhost:8888/mycrm/customer/enrollment/{enroll_obj_id}"
    if request.method=="POST":
        print(request.POST)
        mForm = SalesForms.EnrollmentForm(request.POST)
        if mForm.is_valid():
            try:
                print('hahaha',mForm.cleaned_data)
                #mForm.cleaned_data['customer']=id
                enroll_obj = models.Enrollment.objects.create(**mForm.cleaned_data)
                message['msg']=msg.format(enroll_obj_id=enroll_obj.id)
            except Exception as e:
                enroll_obj = models.Enrollment.objects.get(customer_id=id,enrolled_class_id=mForm.cleaned_data['enrolled_class'])
                mForm.add_error("__all__","此用户已经报名此课程")
                message['msg'] = msg.format(enroll_obj_id=enroll_obj.id)
        else:
            enroll_obj = models.Enrollment.objects.get(customer_id=id,
                                                       enrolled_class_id=mForm.cleaned_data['enrolled_class'])
            mForm.add_error("__all__", "此用户已经报名此课程")
            message['msg'] = msg.format(enroll_obj_id=enroll_obj.id)
    else:
        mForm = SalesForms.EnrollmentForm(initial={'customer':id})
    return HttpResponse(render(request,'myCRM/sales/enroll.html',{'enroll_form':mForm,'message':message}))

class AccountLogin(views.View):
    def get(self,request,*args,**kwargs):
        return HttpResponse(render(request,'myCRM/login.html'))
    def post(self,request,*args,**kwargs):
        _email=request.POST.get("email")
        _password=request.POST.get("password")
        print(_email,_password)
        user=authenticate(username=_email,password=_password)
        print(user)
        if user:
            login(request,user)
            next_url=request.GET.get('next','/mycrm/')
            return HttpResponseRedirect(next_url)
        else:
            errors='wrong!!'
            return HttpResponse(render(request,'myCRM/login.html',{'errors':errors}))

class AccountLogout(views.View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('myCRM:account_login'))
    def post(self,request,*args,**kwargs):
        pass

class CustomerList(views.View):
    def get(self,request,*args,**kwargs):
        return HttpResponse(render(request,'myCRM/sales/customer_list.html'))
    def post(self,request,*args,**kwargs):
        pass
