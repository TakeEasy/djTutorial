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
from django.views.decorators.cache import cache_page
# Create your views here.


class JsonResponse():
    def __init__(self):
        self.status=True
        self.data=None
        self.error=None


def index(request):
    context={
        'hellow':'nihao',
        'isLogin':False
    }
    userID = request.session.get('userID',0)
    userNID = request.session.get('userNID',0)
    print(userID)
    if request.session.get('isLogin',False):
        context['isLogin']=True
        context['userName']=request.session.get('userName','No ONE')
        context['userID']=userID
    allNews=models.News.objects.all()
    for new in allNews:
        new.cssclass1 = "digg-a"
        new.cssclass2 = ""
        favor = models.Favor.objects.filter(favoruser_id=userNID,news_id=new.id)
        if favor:
            new.cssclass1 = "isVoted"
            new.cssclass2 = "vote-actived"
    context['allNews']=allNews

    return HttpResponse(render(request,'chouti/index.html',context))

class SendCodeHandler(views.View):
    def get(self,request,*args,**kwargs):
        return Http404()

    def post(self,request,*args,**kwargs):
        result = JsonResponse()
        sFormObj = AccountForm.SendCodeForm(request.POST)
        flag = sFormObj.is_valid()
        email=request.POST.get('em',None)
        if flag:
            code = common.random_code()
            strEmail = sFormObj.cleaned_data['em']
            try:
                if not models.UserInfo.objects.filter(email=strEmail):
                    limit_time = localtime()-datetime.timedelta(hours=1)
                    if not models.EmailCode.objects.filter(email=strEmail):
                        obj = models.EmailCode(email=email,category='code',content=code,stime=localtime(),status=1)
                        obj.save()
                        message.mail_pass([email,],r"Hi,Your code <Br/> &nbsp;&nbsp;&nbsp;&nbsp;" + code)
                    else:
                        cEmailCode = models.EmailCode.objects.filter(email=strEmail).first()
                        if cEmailCode.stime<limit_time:
                            cEmailCode.stime=localtime()
                            cEmailCode.times=1
                            cEmailCode.content=code
                            cEmailCode.save()
                            message.mail_pass([strEmail, ], r"Hi,Your code <Br/> &nbsp;&nbsp;&nbsp;&nbsp;" + code)
                        elif cEmailCode.times<10:
                            cEmailCode.times=F('times')+1
                            cEmailCode.content = code
                            cEmailCode.stime=localtime()
                            cEmailCode.save()
                            message.mail_pass([strEmail, ], r"Hi,Your code <Br/> &nbsp;&nbsp;&nbsp;&nbsp;" + code)
                        else:
                            result.status=False
                            result.error='一小时内次数太多了!!'

                else:
                    result.status=False
                    result.error='用户已经存在'
            except BaseException as e:
                result.status = False
                result.error = '发送有问题 重试'
                print(str(e))
            finally:
                pass
        else:
            result.status=False
            result.error=sFormObj.errors['em'][0]

        return HttpResponse(json.dumps(result.__dict__))

class RegisterHandler(views.View):
    def get(self,request,*args,**kwargs):
        return Http404()

    def post(self,request,*args,**kwargs):
        result = JsonResponse()
        objRegisterForm = AccountForm.DjRegisterForm(request.POST)
        flag = objRegisterForm.is_valid()
        if not flag:
            result.status = False
            result.error = objRegisterForm.errors.as_data()
            print(objRegisterForm.errors)
            print(objRegisterForm.errors.as_data())
            print(json.dumps(objRegisterForm.errors.as_data(),cls=AccountForm.JsonCustomerEncoder))
        else:
            r = models.EmailCode.objects.filter(email=objRegisterForm.cleaned_data["rgemail"], category="code",content=objRegisterForm.cleaned_data["rgcode"]).order_by('-stime').first()

            if not r:
                result.status = False
                result.error = "code error"
            else:
                try:
                    obj = models.UserInfo(email=objRegisterForm.cleaned_data["rgemail"],
                                              username=objRegisterForm.cleaned_data["rgnick"],
                                              password=common.generate_md5(objRegisterForm.cleaned_data["rgpwd"]),
                                              sex=objRegisterForm.cleaned_data["rgsex"],
                                              region=int(objRegisterForm.cleaned_data["rgregion"]),
                                              sign=objRegisterForm.cleaned_data["rgsign"], ctime=localtime())
                    obj.save()
                    request.session["isLogin"] = True
                    request.session["userID"] = objRegisterForm.cleaned_data["rgemail"]
                    request.session["userName"] = objRegisterForm.cleaned_data["rgnick"]
                    request.session["userNID"] = obj.id
                except BaseException as e:
                    #print("    [Register]: register faild. error msg: ", str(e))
                    result.status = False
                    result.error = str(e)
                finally:
                    pass

        return HttpResponse(json.dumps(result,cls=AccountForm.JsonCustomerEncoder))


class LoginHandler(views.View):
    def get(self,request,*args,**kwargs):
        return Http404

    def post(self,request,*args,**kwargs):
        result = {"status": True, "data": "", "error": ""}
        djloginform=AccountForm.DjLoginForm(request.POST)
        flag = djloginform.is_valid()
        objLoginForm=AccountForm.LoginForm()
        #flag, success_value_dict, error_message_dict = objLoginForm.check_vaild(request)
        if flag:
            formcontent = djloginform.clean()
            user = models.UserInfo.objects.filter(Q(Q(email=formcontent["email"])&Q(password=common.generate_md5(formcontent["empwd"])))|Q(Q(username=formcontent["email"])&Q(password=common.generate_md5(formcontent["empwd"])))).first()
            if user:
                request.session["isLogin"] = True
                request.session["userID"] = formcontent["email"]
                request.session["userName"] = user.username
                request.session["userNID"] = user.id
            else:
                result["status"]=False
                result["error"]="账号密码错误"
        else:
            result["status"]=False
            result["error"]="账号密码格式错误"
            print(djloginform.errors['email'])
            json.dumps(djloginform.errors.as_data(),cls=AccountForm.JsonCustomerEncoder)

        return HttpResponse(json.dumps(result))

class uploadHandler(views.View):
    def get(self,request,*args,**kwargs):
        return Http404

    def post(self,request,*args,**kwargs):
        file_metas = request.FILES("imgUrl")
        ret = {"status": False, "data": "", "error": ""}

        for meta in file_metas:
            file_name = meta["filename"]
            file_ext = file_name.split('.')[1]
            file_path = os.path.join("static","chouti", "uploads", common.generate_random_md5(file_name)) + '.' + file_ext
            with open(file_path, 'wb') as up:
                up.write(meta['body'])
            ret["status"] = True
            ret["data"] = file_path
        return HttpResponse(json.dumps(ret))

class urlTitleHandler(views.View):
    def get(self,request, *args, **kwargs):
        return Http404

    def post(self, request,*args, **kwargs):
        ret = {"status": True, "data": "", "error": "链接不正确"}
        print("[POST]:urlTitle")
        strurl = request.POST.get("rURL", None)
        if re.match('http', strurl) == None:
            strurl = 'http://' + strurl
        strHtml = urlrequest.urlopen(strurl).read()
        title = url.get_title_bs(strHtml)
        description = url.get_description_bs(strHtml)
        ret["title"]=title
        ret["desc"]=description
        return HttpResponse(json.dumps(ret))

class publishHandler(views.View):
    def get(self,request,*args,**kwargs):
        return Http404

    def post(self,request,*args,**kwargs):
        ret = {"status": True, "data": "", "error": "发布失败"}
        userID = request.session.get('userID')
        userNID = request.session.get('userNID')
        kind = request.POST.get('kind')
        if kind=='0':
            strurl = request.POST.get("link", None)
            if re.match('http', strurl) == None:
                strurl = 'http://' + strurl
            obj = models.News(publishuser_id=userNID,
                                  newstype_id=1,
                                  ctime=localtime(),
                                  title=request.POST.get("title", None),
                                  url=strurl,
                                  content=request.POST.get("zhaiyao", None))
            obj.save()
        elif kind=='1':
            obj = models.News(publishuser_id=userNID,
                                  newstype_id=2,
                                  ctime=localtime(),
                                  title="这就是一个段子。。。",
                                  url="",
                                  content=request.POST.get("zhaiyao", None))
            obj.save()
        else:
            obj = models.News(publishuser_id=userNID,
                                  newstype_id=3,
                                  ctime=localtime(),
                                  title="这就是一个图片。。。",
                                  url=request.POST.get("filelink", None),
                                  content=request.POST.get("zhaiyao", None))
            obj.save()
        return HttpResponse(json.dumps(ret))


class dianzanHandler(views.View):
    def get(self,request,*args,**kwargs):
        return Http404

    def post(self,request,*args,**kwargs):
        ret = {"status": True, "data": "", "count": "", "error": ""}
        newID = request.POST.get("newID")
        userID = request.session.get("userNID")
        favor = models.Favor.objects.filter(user_info_id=userID, news_id=newID).first()
        favor.full_clean()
        try:
            if not favor:
                newFavor = models.Favor(favoruser_id=userID, news_id=newID, ctime=localtime())
                newFavor.save()
                ret["data"] = "jiayi"
                ret["count"] = len(models.News.objects.get(pk=newID).first().favors)
            else:
                models.Favor.objects.filter(favoruser_id=userID, news_id=newID).delete()
                ret["data"] = "jianyi"
                ret["count"] = len(models.News.objects.get(pk=newID).first().favors)
        except BaseException as e:
            print("[dianzan]Error")
            ret["status"] = False
            ret["error"] = "something wrong"
        finally:
            pass

        return HttpResponse(json.dumps(ret))

class commentsHandler(views.View):
    def get(self,request,*args,**kwargs):
        return Http404

    def post(self,request,*args,**kwargs):
        newID = request.POST.get('newID', 0)
        ret = {"status": True, "data": "", "count": "", "error": ""}
        comment_list=models.Comment.objects.filter(news_id=newID)


        comment_tree = common.build_tree(comment_list)
        tree_html = common.tree_html(comment_tree)
        ret["data"] = tree_html

        return HttpResponse(json.dumps(ret))


class huifuHandler(views.View):
    def get(self,request,*args,**kwargs):
        return Http404

    def post(self,request,*args,**kwargs):
        newID = request.POST.get('newID', 0)
        who = request.POST.get('who', 0)
        comment = request.POST.get('comment', 0)
        userID = request.session.get("userNID")
        ret = {"status": True, "data": "", "count": "", "error": ""}
        if who != '0':
            newHuifu = models.Comment(userinfo_id=userID, news_id=newID, reply_id=who, up=0, down=0,
                                          device='yijia3t', content=comment, ctime=localtime())
            newHuifu.save()
        else:
            newHuifu = models.Comment(userinfo_id=userID, news_id=newID, reply_id=None, up=0, down=0,
                                          device='yijia3t', content=comment, ctime=localtime())
            newHuifu.save()

        return HttpResponse(json.dumps(ret))

#@cache_page(300)
class djangoFormTest(views.View):
    def get(self,request,*args,**kwargs):
        obj = DjangoTestForm.DjTestForm()
        return HttpResponse(render(request,'chouti/DjTestForm.html',{'obj':obj}))
    def post(self,request,*args,**kwargs):
        obj = DjangoTestForm.DjTestForm(request.POST,request.FILES)
        print(obj.is_valid())
        print(obj.clean())
        print(obj.errors.as_json())
        return HttpResponse(render(request,'chouti/DjTestForm.html',{'obj':obj}))

class djangoModelFormTest(views.View):
    def get(self,request,*args,**kwargs):
        obj = DjangoTestForm.DjTestModelForm()
        return HttpResponse(render(request,'chouti/DjTestModelForm.html',{'obj':obj}))
    def post(self,request,*args,**kwargs):
        obj = DjangoTestForm.DjTestModelForm(request.POST)
        print(obj.is_valid())
        print(obj.clean())
        print(obj.errors.as_json())
        return HttpResponse(render(request,'chouti/DjTestModelForm.html',{'obj':obj}))

class EditdjangoModelFormTest(views.View):
    def get(self,request,nid,*args,**kwargs):
        print('edit get ',nid)
        news_obj=models.News.objects.get(id=nid)
        obj = DjangoTestForm.DjTestModelForm(instance=news_obj)
        return HttpResponse(render(request,'chouti/EditDjTestModelForm.html',{'obj':obj,'newsid':nid}))
    def post(self,request,nid,*args,**kwargs):
        print('edit post ', nid)
        news_obj=models.News.objects.get(id=nid)
        obj = DjangoTestForm.DjTestModelForm(request.POST,instance=news_obj)
        print(obj.is_valid())
        print(obj.clean())
        print(obj.errors.as_json())
        return HttpResponse(render(request,'chouti/EditDjTestModelForm.html',{'obj':obj,'newsid':nid}))

#局部缓存
class cacheTest(views.View):
    def get(self,request,*args,**kwargs):
        import time
        v=time.time()
        return HttpResponse(render(request,'chouti/cacheTest.html',{'V':v}))

#bootstrap测试
class bootstrapTest(views.View):
    def get(self,request,*args,**kwargs):
        return HttpResponse(render(request,'chouti/bootstrapTest.html'))