from django.shortcuts import render,reverse,Http404
from django.http import HttpResponse,HttpResponseRedirect
from django import views
# Create your views here.
from . import crm_admin
import importlib
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .utils import report
from .backend.forms import AutoForm
from django.contrib.auth.decorators import login_required
#from myCRM import models

class Index(views.View):
    def get(self,request,*args,**kwargs):
        print(crm_admin.enabled_admin['myCRM']['customer'].model)
        return HttpResponse(render(request,'crmAdmin/table_index.html',{'enabledAdmin':crm_admin.enabled_admin}))
    def post(self,request,*args,**kwargs):
        return Http404

class DisplayTable(views.View):
    def get(self,request,appname,tablename,*args,**kwargs):
        print('%s ----> %s' % (appname,tablename))
        #model_ogj=importlib.import_module('%s.models.%s'%(appname,tablename))
        admin_class = crm_admin.enabled_admin[appname][tablename]
        print(admin_class.list_display)
        #data_list = admin_class.model.objects.all()
        data_list, condition_filter= report.table_filter(request,admin_class)

        data_list, orderBy = report.table_sort(request,data_list)
        print(orderBy)

        data_list, search_key = report.table_search(request,admin_class,data_list)

        pagintor = Paginator(data_list,admin_class.list_per_page)
        page = request.GET.get('page')
        try:
            data_set = pagintor.get_page(page)
        except PageNotAnInteger:
            data_set = pagintor.get_page(1)
        except EmptyPage:
            data_set = pagintor.get_page(pagintor.num_pages)

        return HttpResponse(render(request,'crmAdmin/table_diaplay.html',{'adminClass':admin_class,'querry_set':data_set,'condition_filter':condition_filter,'order_by':orderBy,'curr_order':request.GET.get('o') or '','searchKey':search_key}))
    def post(self,request,appname,tablename,*args,**kwargs):
        print(request.POST.get('action'))
        print(request.POST.get('selected_ids'))
        strMethod=request.POST.get('action')
        strSelectedIds=request.POST.get('selected_ids','')
        admin_class = crm_admin.enabled_admin[appname][tablename]
        selected_objs = admin_class.model.objects.filter(id__in=strSelectedIds.split(','))

        if hasattr(admin_class,strMethod):
            methodFunc=getattr(admin_class,strMethod)
            return methodFunc(admin_class,request,selected_objs)

        data_list, condition_filter = report.table_filter(request, admin_class)
        data_list, orderBy = report.table_sort(request, data_list)
        data_list, search_key = report.table_search(request, admin_class, data_list)
        pagintor = Paginator(data_list, admin_class.list_per_page)
        page = request.GET.get('page')
        try:
            data_set = pagintor.get_page(page)
        except PageNotAnInteger:
            data_set = pagintor.get_page(1)
        except EmptyPage:
            data_set = pagintor.get_page(pagintor.num_pages)


        return HttpResponse(render(request,'crmAdmin/table_diaplay.html',{'adminClass':admin_class,'querry_set':data_set,'condition_filter':condition_filter,'order_by':orderBy,'curr_order':request.GET.get('o') or '','searchKey':search_key}))

class ChangeTable(views.View):
    def get(self,request,appname,tablename,id,*args,**kwargs):
        admin_class = crm_admin.enabled_admin[appname][tablename]
        dyModelClass = AutoForm.create_model_form(request,admin_class)
        dyModelObj = dyModelClass(instance=admin_class.model.objects.get(id=id))
        return HttpResponse(render(request,'crmAdmin/table_change.html',{'adminClass':admin_class,'dyModelObj':dyModelObj,'appname':appname,'tablename':tablename,'addTable':False}))
    def post(self,request,appname,tablename,id,*args,**kwargs):
        admin_class = crm_admin.enabled_admin[appname][tablename]
        dyModelClass = AutoForm.create_model_form(request, admin_class)
        dataObj = admin_class.model.objects.get(id=id)
        dyModelObj = dyModelClass(request.POST,instance=dataObj)
        if dyModelObj.is_valid():
            dyModelObj.save()
        else:
            #dyModelObj = dyModelClass(instance=dataObj)
            pass

        return HttpResponse(render(request,'crmAdmin/table_change.html',{'adminClass':admin_class,'dyModelObj':dyModelObj,'appname':appname,'tablename':tablename}))

class AddTable(views.View):
    def get(self,request,appname,tablename,*args,**kwargs):
        admin_class = crm_admin.enabled_admin[appname][tablename]
        dyModelClass = AutoForm.create_model_form(request,admin_class)
        dyModelObj = dyModelClass()
        return HttpResponse(render(request,'crmAdmin/table_add.html',{'adminClass':admin_class,'dyModelObj':dyModelObj,'addTable':True}))

    def post(self,request,appname,tablename,*args,**kwargs):
        admin_class=crm_admin.enabled_admin[appname][tablename]
        dyModelClass=AutoForm.create_model_form(request, admin_class)
        dyModelObj = dyModelClass(request.POST)
        if dyModelObj.is_valid():
            dyModelObj.save()
            return HttpResponseRedirect(reverse('crmAdmin:table_display', args=(appname,tablename)))
        else:
            dyModelObj = dyModelClass()
        return HttpResponse(render(request, 'crmAdmin/table_add.html', {'adminClass': admin_class, 'dyModelObj': dyModelObj}))

class DeleteTable(views.View):
    def get(self,request,appname,tablename,id,*args,**kwargs):
        admin_class= crm_admin.enabled_admin[appname][tablename]
        dataObj=admin_class.model.objects.get(id=id)
        if admin_class.readonly_table:
            errors="Read Only table you can't delete!!"
        else:
            errors=""
        return HttpResponse(render(request,'crmAdmin/table_delete.html',{'adminClass':admin_class,'dataObj':[dataObj,],'appname':appname,'tablename':tablename,'errors':errors}))
    def post(self,request,appname,tablename,id,*args,**kwargs):
        admin_class = crm_admin.enabled_admin[appname][tablename]
        dataObj = admin_class.model.objects.get(id=id)
        if dataObj and not admin_class.readonly_table:
            dataObj.delete()
        return HttpResponseRedirect(reverse('crmAdmin:table_display',args=(appname,tablename)))

class ChangePassword(views.View):
    def get(self,request,appname,tablename,id,*args,**kwargs):
        admin_class=crm_admin.enabled_admin[appname][tablename]
        dataObj = admin_class.model.objects.get(id=id)
        errors=""
        return HttpResponse(render(request,'crmAdmin/table_changepwd.html',{'adminClass':admin_class,'dataObj':dataObj,'appname':appname,'tablename':tablename,'errors':errors}))
    def post(self,request,appname,tablename,id,*args,**kwargs):
        admin_class=crm_admin.enabled_admin[appname][tablename]
        dataObj=admin_class.model.objects.get(id=id)
        errors=""
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1==password2:
            dataObj.set_password(password1)
            dataObj.save()
            HttpResponseRedirect(reverse('crmAdmin:table_change',args=(appname,tablename,id)))
        else:
            errors="Two password input not equal."
        return HttpResponse(render(request,'crmAdmin/table_changepwd.html',{'adminClass':admin_class,'dataObj':dataObj,'appname':appname,'tablename':tablename,'errors':errors}))