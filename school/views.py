from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from django import views
import json

#将函数装饰器转换成方法装饰器
from django.utils.decorators import method_decorator


# Create your views here.

def auth(func):
    def inner(request, *args, **kwargs):
        if request.session.get('isLogin', False):
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('school:login'))
    return inner

def outerTest(func):
    def inner(request,*args,**kwargs):
        print(request.method)
        return func(request,*args,**kwargs)
    return inner

@auth
def index(request):
    context = {
        'username': '',
    }
    context['username'] = request.session.get('username')
    print(context['username'])
    return HttpResponse(render(request, 'school/index.html', context))
    # return HttpResponse(render(request,'school/index.html',context))


# def login(request):
#     context = {
#         'msg': ''
#     }
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         print(username, password)
#         admin = models.Administrator.objects.filter(username=username, password=password)
#         if admin.exists():
#             ret = HttpResponseRedirect(reverse('school:index'))
#             # ret.set_cookie('islogin',True,max_age=100)
#             # ret.set_cookie('username',username,max_age=100)
#             request.session['isLogin'] = True
#             request.session['username'] = username
#             return ret
#         else:
#             context['msg'] = 'username or password error!!'
#     return HttpResponse(render(request, 'school/login.html', context))

class Login(views.View):
    #对请求做处理用dispatch方法
    def dispatch(self, request, *args, **kwargs):
        print('1111111')
        ret = super(Login,self).dispatch(request,*args,**kwargs)
        print('2222222')
        return ret

    #对莫一种请求处理用这种装饰器
    @method_decorator(outerTest)
    def get(self,request,*args,**kwargs):
        context = {
            'msg':''
        }
        return HttpResponse(render(request,'school/login.html',context))

    @method_decorator(outerTest)
    def post(self,request,*args,**kwargs):
        context = {
            'msg':''
        }
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        admin = models.Administrator.objects.filter(username=username, password=password)
        if admin.exists():
            ret = HttpResponseRedirect(reverse('school:index'))
            # ret.set_cookie('islogin',True,max_age=100)
            # ret.set_cookie('username',username,max_age=100)
            request.session['isLogin'] = True
            request.session['username'] = username
            return ret
        else:
            context['msg'] = 'username or password error!!'
            return HttpResponse(render(request,'school/login.html',context))

def logout(request):
    request.session.clear()
    return HttpResponseRedirect(reverse('school:login'))

class PageHelper():
    def __init__(self,total_count,page,base_url):
        self.total_count = total_count
        self.page = page
        self.base_url = base_url

    def get_startpage(self):
        return (self.page-1)*10

    def get_endpage(self):
        return self.page*10

    def get_totalpage(self):
        v, a = divmod(self.total_count, 10)
        if a != 0:
            v += 1
        return v

    def get_pageHtml(self):
        v, a = divmod(self.total_count, 10)
        if a != 0:
            v += 1

        if v <= 11:
            pagerange_start = 1
            pagerange_end = v + 1
        else:
            if self.page < 6:
                pagerange_start = 1
                pagerange_end = 12
            elif self.page > v - 5:
                pagerange_start = v - 10
                pagerange_end = v + 1
            else:
                pagerange_start = self.page - 5
                pagerange_end = self.page + 6
        page_list = []
        for i in range(pagerange_start, pagerange_end):
            if i == self.page:
                page_list.append("<a href='%s?p=%s' style='background-color:black;' >%s</a>" % (self.base_url,i, i))
            else:
                page_list.append("<a href='%s?p=%s'>%s</a>" % (self.base_url,i, i))

        page_html = " ".join(page_list)
        return page_html




@auth
def classadmin(request):
    if request.method=="GET":
        context = {
            'username':request.session['username']
        }
        page = request.GET.get('p',1)
        page = int(page)
        total_count = models.Classes.objects.all().count()
        pageObj = PageHelper(total_count,page,'/school/classadmin')


        start = pageObj.get_startpage()
        end = pageObj.get_endpage()
        cls_list = models.Classes.objects.all()[start:end]
        context['cls_list'] = cls_list
        page_html = pageObj.get_pageHtml()


        context['page_html'] = page_html
        return HttpResponse(render(request,'school/classadmin.html',context))
    elif request.method=="POST":
        caption = request.POST.get('caption',None)
        result_dic = {'status':True,'error':None,'data':None}
        if caption:
            obj = models.Classes.objects.create(caption=caption)
            result_dic['data'] = {'id':obj.id,'caption':obj.caption}
        else:
            result_dic['status'] = False
            result_dic['error'] = 'can not be null or empty!'
        #return HttpResponseRedirect(reverse(request,'school:classadmin'))
        return HttpResponse(json.dumps(result_dic))

@auth
def teacheradmin(request):
    context = {
        'username': request.session['username']
    }
    return HttpResponse(render(request,'school/teacheradmin.html',context))

@auth
def studentadmin(request):
    context = {
        'username': request.session['username']
    }
    return HttpResponse(render(request,'school/studentadmin.html',context))

