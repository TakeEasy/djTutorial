# -*- coding:utf-8 -*-
# Author:YEAR
from django.db.models import Q

def table_filter(request,admin_class):
    filter_condition={}
    for k,v in request.GET.items():
        if k in ['page','o','search']:
            continue
        if v:
            filter_condition[k]=v

    return admin_class.model.objects.filter(**filter_condition).order_by(admin_class.ordering or "-id"),filter_condition

def table_sort(request,tabledata):
    orderby=request.GET.get('o')
    if orderby:
        tabledata = tabledata.order_by(orderby)
        if orderby.startswith('-'):
            orderby=orderby.strip('-')
        else:
            orderby='-'+orderby
    return tabledata,orderby

def table_search(request,admin_class,tabledata):
    search_key=request.GET.get('search','')
    tableQ=Q()
    tableQ.connector="OR"
    for field in admin_class.search_fields:
        tableQ.children.append(("%s__contains"%field,search_key))

    return tabledata.filter(tableQ),search_key

def rescursive_related_objs(objs):
    ul_ele="<ul>"
    for obj in objs:
        li_ele='''<li>%s : %s</li>'''%(obj._meta.verbose_name,obj.__str__().strip("<>"))
        ul_ele+=li_ele

        for m2m_obj in obj._meta.local_many_to_many:
            ul_m2m="<ul>"
            m2m_field_object=getattr(obj,m2m_obj.name)
            for field in m2m_field_object.all():
                li_m2m='''<li>%s %s</li>'''%(m2m_obj.verbose_name,field.__str__().strip("<>"))
                ul_m2m+=li_m2m
            ul_m2m+="</ul>"
            ul_ele+=ul_m2m

        for relate_obj in obj._meta.related_objects:
            if 'ManyToOneRel' not in relate_obj.__repr__():
                continue
            if hasattr(obj,relate_obj.get_accessor_name()):
                accessor_obj=getattr(obj,relate_obj.get_accessor_name())
                rescursive_obj=accessor_obj.all()
            else:
                continue
            if len(rescursive_obj)>0:
                nodes = rescursive_related_objs(rescursive_obj)
                ul_ele +=nodes
    ul_ele+='''</ul>'''
    return ul_ele