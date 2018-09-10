# -*- coding:utf-8 -*-
# Author:YEAR
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

class mdTest1(MiddlewareMixin):
    def process_request(self,request):
        print('mdTest1------>request')

    def process_view(self,request,view_func,view_args,view_kwargs):
        print(view_func,view_args,view_kwargs)
        print('mdTest1------>View')

    def process_response(self,request,response):
        print('mdTest1------>response')
        return response

    def process_exception(self,request,exception):
        print('mdTest1------>exception')

    def process_template_response(self,request,response):#没什么卵用只有返回对象有render方法的时候才会调用
        print('mdTest1------>template_response')
        return response

class mdTest2(MiddlewareMixin):
    def process_request(self,request):
        print('mdTest2------>request')
    def process_response(self,request,response):
        print('mdTest2------>response')
        #print(type(response))
        return response

class mdTestOver(MiddlewareMixin):
    def process_request(self,request):
        print('mdTest1------>request')
        return HttpResponse('Over....')
    def process_response(self,request,response):
        print('mdTest1------>response')
        return response