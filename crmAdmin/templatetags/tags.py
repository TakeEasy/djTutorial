# -*- coding:utf-8 -*-
# Author:YEAR
from django import template
from django.utils.safestring import mark_safe
#from datetime import datetime
from django.utils.timezone import datetime,timedelta
from crmAdmin.utils import report
from django.core.exceptions import FieldDoesNotExist

register = template.Library()

@register.simple_tag
def render_table_name(admin_class):
    return admin_class.model._meta.verbose_name

@register.simple_tag
def render_table_set(admin_class):
    return admin_class.model.objects.all()

@register.simple_tag
def build_table_row(request,obj,admin_class):
    row_html=''
    for strcolumn in admin_class.list_display:
        field_obj = obj._meta.get_field(strcolumn)
        if field_obj.choices:
            tddata=getattr(obj,'get_%s_display'%strcolumn)()
        else:
            tddata = getattr(obj,strcolumn)
        if type(tddata).__name__=="datetime":
            tddata = datetime.fromtimestamp(tddata.timestamp())
            tddata = tddata.strftime("%Y-%m-%d %H:%M:%S")

        row_html += "<td>%s</td>" % tddata

    editUrl="%s/%s/change"%(request.path,obj.id)
    row_html +="<td><a href='%s'><span class='fa fa-edit'></span></a></td>"%editUrl

    for actionButton in admin_class.action_buttons:
        actionButtonEle=getattr(obj,actionButton)(obj.id)
        row_html += "<td>%s</td>"%actionButtonEle

    return mark_safe(row_html)

@register.simple_tag
def build_page_list(currentpage,pageObj,condition_filter):
    pageliHtml=""
    isactive=""
    urlconditionHtml=""
    for k,v in condition_filter.items():
        urlconditionHtml+="&%s=%s"%(k,v)
    if abs(pageObj.number - currentpage)<=2:
        if pageObj.number==currentpage:
            isactive="active"
        pageliHtml='<li class="page-item %s"><a class="page-link" href="?page=%s%s">%s</a></li>'%(isactive,currentpage,urlconditionHtml,currentpage)

    return mark_safe(pageliHtml)

@register.simple_tag
def build_all_page(pageObj,condition_filter,curr_order,search_key):
    pageliHtml = ""
    isactive=""
    urlconditionHtml=""
    ignorePage=True
    for k,v in condition_filter.items():
        urlconditionHtml+="&%s=%s"%(k,v)

    #print(pageObj.paginator.page_range)
    for pageNum in pageObj.paginator.page_range:
        if pageNum<3 or pageNum>pageObj.paginator.num_pages-2 \
            or abs(pageObj.number-pageNum)<=2:
            if pageObj.number==pageNum:
                isactive="active"
                ignorePage=True
            else:
                isactive=""

            pageliHtml+='<li class="page-item %s"><a class="page-link" href="?page=%s%s&o=%s&search=%s">%s</a></li>'%(isactive,pageNum,urlconditionHtml,curr_order,search_key,pageNum)
        else:
            if ignorePage:
                pageliHtml+='<li><a>...</a></li>'
                ignorePage=False
    return mark_safe(pageliHtml)

@register.simple_tag
def render_table_head(column,sort_by,condition_filter,search_key,adminClass):
    urlconditionHtml = ""
    sortHtml=""
    for k, v in condition_filter.items():
        urlconditionHtml += "&%s=%s" % (k, v)
    theadHtml="<th><a href='?o={sortBy}{condition}{searchKey}'>{column}</a><span style='float:right' class='{spanClass}' ></span></th>"
    if sort_by:
        if column==sort_by.strip('-'):
            sortHtml=sort_by
            if sort_by.startswith('-'):
                spanClass = "fa fa-sort-up"
            else:
                spanClass = "fa fa-sort-down"
        else:
            spanClass=""
            sortHtml = column
    else:
        spanClass=""
        sortHtml=column
    search_key="&search=%s"%search_key
    return mark_safe(theadHtml.format(sortBy=sortHtml,condition=urlconditionHtml,column=adminClass.model._meta.get_field(column).verbose_name,spanClass=spanClass,searchKey=search_key))



@register.simple_tag
def render_condition_url(condition_filter):
    urlconditionHtml=""
    for k,v in condition_filter.items():
        urlconditionHtml+="&%s=%s"%(k,v)
    return urlconditionHtml


@register.simple_tag
def render_filter_condition(condition,admin_class,condition_filter):
    conditionSelectHtml="<select class='form-control' name=%s>"%condition
    #print("----------------------%s"%condition)
    fieldObj = admin_class.model._meta.get_field(condition)
    #print("----------------------%s"%fieldObj)
    #print(condition_filter)
    if fieldObj.choices:
        for choice_item in fieldObj.get_choices():
            selected=''
            if condition_filter.get(condition)==str(choice_item[0]):
                selected='selected'
            conditionSelectHtml += "<option value='%s' %s >%s</option>"%(choice_item[0],selected,choice_item[1])

    if type(fieldObj).__name__=="ForeignKey":
        for choice_item in fieldObj.get_choices():
            selected = ''
            if condition_filter.get(condition) == str(choice_item[0]):
                selected = 'selected'
            conditionSelectHtml += "<option value='%s' %s >%s</option>" % (choice_item[0],selected, choice_item[1])

    if type(fieldObj).__name__ in ["DateTimeField","DateField"]:
        conditionSelectHtml = "<select class='form-control' name=%s__gte>" % condition
        date_els=[]
        today_ele=datetime.now().date()
        date_els.append(['Today',today_ele])
        date_els.append(['Yesterday',today_ele-timedelta(1)])
        date_els.append(['A Week',today_ele-timedelta(7)])
        date_els.append(['Month',today_ele-timedelta(30)])
        conditionSelectHtml += "<option value='%s' %s >%s</option>" % ('', '', '---------')
        for item in date_els:
            selected=''
            #print(condition_filter.get("%s__gte"%condition))
            if condition_filter.get("%s__gte"%condition) == item[1].__str__():
                selected="selected"
            conditionSelectHtml += "<option value='%s' %s >%s</option>"%(item[1],selected,item[0])
    conditionSelectHtml+="</select>"
    #print("------------------------%s"%conditionSelectHtml)
    return mark_safe(conditionSelectHtml)

@register.simple_tag
def get_m2m_objlist(admin_class,fieldName,formObj):
    fieldObj=getattr(admin_class.model,fieldName)
    allObj = fieldObj.rel.model.objects.all()
    #print('----',formObj.instance)
    if getattr(formObj.instance,'id'):
        chosenObj = getattr(formObj.instance,fieldName).all()
    else:
        return allObj
    avliableObj=[]
    for obj in allObj:
        if obj not in chosenObj:
            avliableObj.append(obj)
    return avliableObj

@register.simple_tag
def get_m2m_chosenobjlist(formObj,fieldName):
    if getattr(formObj.instance,'id'):
        fieldObj=getattr(formObj.instance,fieldName)
    else:
        return []
    return fieldObj.all()

@register.simple_tag
def get_delete_info(dataObj):
    html=report.rescursive_related_objs(dataObj)
    return mark_safe(html)
