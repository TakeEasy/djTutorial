/**
 * Created by YEAR on 2017/9/14.
 */
//使用如下格式形成闭包环境
(function ($) {
    chouti={
        Init:function () {
            chouti.ShowLoginDialog();
            chouti.HideLoginDialog();
            chouti.BindGetCode();
            chouti.showUserOprBox();
            chouti.loginChouti();
            chouti.publishChouti();
            chouti.bindPublishEvent();
            chouti.changeTabPublish();
            chouti.changePicPublishTo();
            chouti.uploadPic();
            chouti.bindTipsEvent($("#txt-zixun"));
            chouti.bindTipsEvent($("#txt-duanzi"));
            chouti.bindTipsEvent($("#txt-img"));
            chouti.bindPubButtonAndSumChar(0);
            chouti.bindAllNewsAction();
            //chouti.bindPubButtonAndSumChar(1);
            //chouti.bindPubButtonAndSumChar(2);

        },
        ShowLoginBox:function (e) {
            $(".module-login-mask").show();
            $(".module-login-mask").find(".box-active").removeClass("box-active");
            e ? ($(".module-login-mask").find(".box-register").find(".header").eq(1).addClass("box-active"), $(".module-login-mask").find(".rgemail").focus()) : ($(".module-login-mask").find(".box-login").find(".header").addClass("box-active"), 2 == localStorage.getItem("logintype") ? $(".module-login-mask").find(".userid").focus() : $(".module-login-mask").find(".email").focus())
        },
        HideLoginBox:function () {
            $(".module-login-mask").hide();
        },
        ShowLoginDialog:function () {
            $('#reg-link-a').click(function () {
                chouti.ShowLoginBox('reg');
            });
            $('#login-link-a').click(function () {
                chouti.ShowLoginBox();
            })
        },
        HideLoginDialog:function () {
            $(".module-login-mask .dialog-btn-close").click(function () {
                chouti.HideLoginBox();
            })
        },
        intCountDown:10,
        SendMailCountdown:function () {
            var btnSendCode=$('.box-register-email .btn-getcode');
            if (chouti.intCountDown==0){
                btnSendCode.prop("disabled",false);
                btnSendCode.removeClass("btn-disable");
                btnSendCode.css("cursor","default");
                btnSendCode.click(function () {
                    chouti.GetCode(this);
                });
                btnSendCode.text("获取验证码");
                console.log("倒计时结束");
                chouti.intCountDown=10;
                clearTimeout();
            }
            else {
                setTimeout(chouti.SendMailCountdown,1000);
                btnSendCode.prop("disabled",true);
                btnSendCode.addClass("btn-disable");
                btnSendCode.css("cursor","wait");
                btnSendCode.unbind('click');
                btnSendCode.text(chouti.intCountDown);
                console.log(chouti.intCountDown);
                chouti.intCountDown--;
            }
        },
        GetCode:function (ths) {
            var email = $(ths).prev().val();
            console.log(email);
            $.ajax({
                url:'/chouti/send_code/',
                type:'POST',
                data:{em:email},
                success:function (arg) {
                    ret=JSON.parse(arg);
                    console.log(ret);
                    if (ret.status){
                        chouti.SendMailCountdown();
                    }
                    else {
                        alert('发送验证码失败,请重试');
                        console.log('发送验证码失败..');
                    }
                },
                error:function (arg) {
                    alert('发送验证码失败,请重试')
                    console.log('发送验证码失败..')
                }
            })
        },
        BindGetCode:function () {
            $(".box-register-email .btn-getcode").click(function () {
                chouti.GetCode(this);
            })
        },
        ShowRegisterEmail:function () {
            $(".box-register-detail").hide();
            $(".box-register-email").show();
        },
        ShowRegisterDetail:function () {
            $(".box-register-email").hide();
            $(".box-register-detail").show();
        },
        RegisterChouti:function () {
            $("#btnrg span").eq(0).hide();
            $("#btnrg span").eq(1).show();
            var post_dict={};
            $(".body-register .register-content").each(function () {
                var input_val=$(this).val();
                var input_name=$(this).attr('name');
                post_dict[input_name]=input_val;
            });
            $('input.sex:checked')
            post_dict[$('input.sex:checked').attr('name')]=$('.sex:checked').val();
            console.log(post_dict);
            $.ajax({
                url:"/chouti/register/",
                type:'POST',
                data:post_dict,
                success:function (arg) {
                    ret=JSON.parse(arg);
                    console.log(ret);
                    $("#btnrg span").eq(0).show();
                    $("#btnrg span").eq(1).hide();
                    if(ret.status){
                        location.reload();
                    }
                    else {
                        alert("注册失败 原因:"+ret.error);
                    }
                },
                error:function (arg) {
                    $("#btnrg span").eq(0).show();
                    $("#btnrg span").eq(1).hide();
                }
            });
        },
        showUserOprBox:function () {
            $("#loginUserNc").hover(function () {
                var e = $("#userOprBox"), t=$(".key-sera").offset().left;
                //console.log("key-sera offset"+t);
                t-=127;
                e.css("left",t+"px").show();
            }, function () {
                e.hide();
            });

            var e = $("#userOprBox");
            e.hover(function () {
                e.show();
            },function () {
                e.hide();
            })
        },
        loginChouti:function () {
            $("#btnLogin").click(function () {
                $("#btnLogin span").eq(0).hide();
                $("#btnLogin span").eq(1).show();
                post_dict={};
                $(".box-emaillogin .login-content").each(function () {
                   var input_val=$(this).val();
                   var input_name=$(this).attr("name");
                   post_dict[input_name]=input_val;
                });
                console.log(post_dict);
                $.ajax({
                    url:"/chouti/login/",
                    type:"POST",
                    data:post_dict,
                    success:function (arg) {
                        var ret=JSON.parse(arg);
                        console.log(ret);
                        if(ret.status){
                            location.reload();
                        }
                        else {
                            $("#btnLogin span").eq(0).show();
                            $("#btnLogin span").eq(1).hide();
                            alert("登陆失败 原因:"+ret.error)
                        }
                    },
                    error:function (arg) {

                    }
                })
            })
        },
        showMask:function (e,t) {
            var n = $("body").height(), i = $("body").width();
            var o = parseInt(i / 2) - parseInt($(e).width() / 2), s = parseInt(a / 2) - parseInt($(e).height() / 2) + parseInt($(window).scrollTop());
            var a = document.documentElement.clientHeight || document.body.clientHeight;
            ""==t?$(e).css({left:o,top:s}):$(e).css({left:o});
            n = parseInt($("body").height());
            a = parseInt(a);
            n = n > a ? n : a;
            var mask = "<div class='op mask' id='mask' style='width: " + i + "px; height: " + n + "px;filter: alpha(opacity=50)'></div>";
            $("body").append(mask);
        },
        showPublishBox:function () {
            chouti.showMask("#digg-dialog-publish", "top");
            $("#mask").show();
            $("#digg-dialog-publish").show().css("top", "130px");
        },
        hidePublishBox:function () {
            $("#mask").hide().remove();
            $("#digg-dialog-publish").hide();
        },
        bindPublishEvent:function () {
            $("#digg-dialog-publish .dialog-titlebar-close").click(function () {
                chouti.hidePublishBox();
            })
        },
        changePicPublishTo:function () {
            $("#publish-content-zixun .toclass-btn-area a").click(function () {
                    $(this).removeClass("toclass-btn-unvalid").addClass("toclass-btn-valid").siblings().removeClass("toclass-btn-valid").addClass("toclass-btn-unvalid");
                });
            $("#publish-content-duanzi .toclass-btn-area a").click(function () {
                    $(this).removeClass("toclass-btn-unvalid").addClass("toclass-btn-valid").siblings().removeClass("toclass-btn-valid").addClass("toclass-btn-unvalid");
                });
            $("#publish-content-pic .toclass-btn-area a").click(function () {
                    $(this).removeClass("toclass-btn-unvalid").addClass("toclass-btn-valid").siblings().removeClass("toclass-btn-valid").addClass("toclass-btn-unvalid");
                });
        },
        changeTabPublish:function () {
            $("#pubTabZixun").click(function () {
                $(this).addClass("w-active color").siblings().removeClass("w-active color");
                var e = $("#tabs a").index(this);
                $("#dialog-main-content").children().eq(e).show().siblings().hide();
                $("#to-btn-duanzi2").addClass("toclass-btn-valid").removeClass("toclass-btn-unvalid");
                chouti.bindPubButtonAndSumChar(0);
            });
            $("#pubTabDuanzi").click(function () {
                $(this).addClass("w-active color").siblings().removeClass("w-active color");
                var e = $("#tabs a").index(this);
                $("#dialog-main-content").children().eq(e).show().siblings().hide();
                $("#to-btn-duanzi2").addClass("toclass-btn-valid").removeClass("toclass-btn-unvalid");
                chouti.bindPubButtonAndSumChar(1);
            });
            $("#pubTabPic").click(function () {
                $(this).addClass("w-active color").siblings().removeClass("w-active color");
                var e = $("#tabs a").index(this);
                $("#dialog-main-content").children().eq(e).show().siblings().hide();
                $("#to-btn-duanzi2").addClass("toclass-btn-valid").removeClass("toclass-btn-unvalid");
                chouti.bindPubButtonAndSumChar(2);
            });
        },
        publishChouti:function () {
            if($("#loginUserNc").length>0){
                $("#btnPublish").click(function () {
                    chouti.showPublishBox();
                })
            }
            else {
                $("#btnPublish").click(function () {
                    chouti.ShowLoginBox();
                })
            }
        },
        uploadPicComplete:function () {
            var origin = $("#uploadIframe").contents().find("body").text();
            var obj = JSON.parse(origin);
            console.log(obj);
            if(obj.status){
                $("#upload-img").attr("src",obj.data);
                $("#upload-img-area").hide();
                $("#show-img-area").show();
            }
            else{
                alert("上传失败咯傻逼!!");
            }
        },
        uploadPic:function () {
            console.log("bind onchange!!");
            $("#imgUrl").on("change",function () {
                $("#uploadIframe").on("load",chouti.uploadPicComplete);
                $("#uploadPicFrm").target="uploadIframe";
                $("#uploadPicFrm").submit();
            });
            $("#repeat-upload-btn").click(function () {
                $("#upload-img").attr("src","");
                $("#imgUrl").val("");
                $("#show-img-area").hide();
                $("#upload-img-area").show();
            })
        },
        //绑定在光标移入移出input框的时候label的消失和显示
        bindTipsEvent:function (t) {
            return t.focus(function () {
                var t = $(this), n = t.attr("id"), i = t.siblings("label[for='" + n + "']");
                i.hide()
            }).blur(function () {
                var t = $(this), n = t.attr("id"), i = t.siblings("label[for='" + n + "']");
                "" === $.trim(t.val()) && i.show()
            })
        },
        //设置发布按钮可以使用
        setPubButtonAbled:function (e) {
            $("#pub-btn" + e).addClass("new-pub-btn-valid").removeClass("new-pub-btn-unvalid").prop("disabled",false);
            "" == $.trim($("#txt-zixun-content").val()) && $("#pub-btn0").addClass("new-pub-btn-unvalid").removeClass("new-pub-btn-valid").prop("disabled",true);
            0 == e && $("#add-pub-btn" + e).addClass("pub-btn-valid").removeClass("pub-btn-unvalid").prop("disabled",false);
        },
        //设置发布按钮不能使用
        setPubButtonDisabled:function(e){
            $("#pub-btn" + e).addClass("new-pub-btn-unvalid").removeClass("new-pub-btn-valid").prop("disabled",true);
            "" != $.trim($("#txt-zixun-content").val()) && $("#pub-btn0").addClass("new-pub-btn-valid").removeClass("new-pub-btn-unvalid").prop("disabled",false);
            0 == e && $("#add-pub-btn" + e).addClass("pub-btn-unvalid").removeClass("pub-btn-valid").prop("disabled",true);
        },
        //去除前后空格
        clearBeforeNull:function(e){
            var t= /^(\s+)|(\s+)$/,n=e;
            return n=n.replace(t,""),n=n.replace(t,"");
        },
        //去除中间多余空格
        clearMidNull:function (e) {
            var t=/\s+/g, n=e.replace(t," ");
            return n;
        },
        //计算发布咨询的字数,并做出相应的反应
        countZixunLength:function (e,t) {
            console.log(e);
            var e = chouti.clearBeforeNull(e);
            e = chouti.clearMidNull(e);
            console.log(e);
            for (var n = 0, i=0;i<e.length;i++){
                var o = e.charCodeAt(i);
                o>=1&&o<=126||65376<=o && o<=65439 ?n++:n+=2
            }
            var a = parseInt(n/2),s=n%2;
            0!=s && (a+=1);
            if (a!=0){
                //添加获取标题按钮事件
                $("#add-pub-btn0").off("click");
                $("#add-pub-btn0").on("click",chouti.addLink);
                //添加清空按钮事件
                $("#clear-btn-link").off("click");
                $("#clear-btn-link").on("click",chouti.clearPublish);
                //添加发布按钮事件
                $("#pub-btn0").off("click");
                $("#pub-btn0").on("click",chouti.publishSomeThing);
            }
            else {
                //删除获取标题按钮事件
                $("#add-pub-btn0").off("click");
                //删除清空按钮事件
                $("#clear-btn-link").off("click");
                //删除发布按钮事件
                $("#pub-btn0").off("click");

            }
            var r = 150-a;
            r<0?$("#write-error-box0 .write-error-desc").html("链接过长，重新输入！！").show():$("#write-error-box0 .write-error-desc").hide();
        },
        //计算发布段子的字数并,做出相应的反应
        countDuanziLength:function (e,t) {
            var e = chouti.clearBeforeNull(e);
            e=chouti.clearMidNull(e);
            for ( var n =0,i=0;i<e.length;i++){
                var o=e.charCodeAt(i);
                o>=1&&o<=126||65376<=o&&o<=65439?n++:n+=2
            }
            var a = parseInt(n/2),s=n%2;
            0!=s && (a+=1);
            if (a!=0){
                //添加清空按钮事件
                $("#clear-btn-wanzi").off("click");
                $("#clear-btn-wanzi").on("click",chouti.clearPublish);
                $("#clear-btn-pic").off("click");
                $("#clear-btn-pic").on("click",chouti.clearPublish);
                //添加发布按钮事件
                $("#pub-btn1").off("click");
                $("#pub-btn1").on("click",chouti.publishSomeThing);
                $("#pub-btn2").off("click");
                $("#pub-btn2").on("click",chouti.publishSomeThing);
            }
            else {
                //删除清空按钮事件
                $("#clear-btn-wanzi").off("click");
                $("#clear-btn-pic").off("click");
                $("#pub-btn1").off("click");
                $("#pub-btn2").off("click");
            }
            var r = 150-a;
            $("#showLength" + t).html(r),r < 0 ? ($("#moreLength" + t).html(-r), $("#dialog-buttonpane" + kind + " .write-error").show(), $("#showLength" + t).html(0), $("#dialog-buttonpane" + kind + " .write-length").hide()) : ($("#dialog-buttonpane" + kind + " .write-error").hide(), $("#dialog-buttonpane" + kind + " .write-length").show())
        },
        inputState:function () {
            var e=kind,t=$(obj).val();
            console.log(kind);
            console.log(obj);
            if (""==$.trim(t))return chouti.setPubButtonDisabled(e),void $("#showLength"+e).html(150);
            switch (chouti.setPubButtonAbled(e),e){
                case 0:
                    chouti.countZixunLength(t,e);
                    break;
                case 1:
                    chouti.countDuanziLength(t,e);
                    break;
                case 2:
                    chouti.countDuanziLength(t,e);
                    break;
            }
        },
        //绑定发布框内的按钮是否可点击和字数统计
        bindPubButtonAndSumChar:function (e) {
            switch(chouti.setPubButtonDisabled(e),$("#showLength" + e).html(150),e){
                case 0:
                    console.log('zixun');
                    obj = "#txt-zixun", kind=0,$("#txt-zixun").on("input propertychange", chouti.inputState);
                    break;
                case 1:
                    console.log('duanzi');
                    obj = "#txt-duanzi", kind=1,$("#txt-duanzi").on("input propertychange", chouti.inputState);
                    break;
                case 2:
                    console.log('img');
                    obj = "#txt-img", kind=2,$("#txt-img").on("input propertychange", chouti.inputState);
                    break;
            }
        },
        //发布资讯页面获取标题按钮的click事件
        addLink:function () {
            var e = $.trim($("#txt-zixun").val());
            if ("" != e){
                $("#add-pub-loading0").css("display","block");
                $("#add-pub-btn0").css("display","none");
                //$("#txt-zixun").prop("disabled",true);
                post_dict={};
                post_dict["rURL"]=e;
                $.ajax({
                    url:"/chouti/urltitle/",
                    type:"post",
                    data:post_dict,
                    success:function (arg) {
                        var ret=JSON.parse(arg);
                        if(ret.status==true) {
                            console.log(ret.title);
                            console.log(ret.desc);
                            $("#add-pub-loading0").css("display","none");
                            $("#txt-zixun-content").val(ret.title);
                            $("#txt-zhaiyao").val(ret.desc);
                            $("#txt-zixun").attr("disabled", !0).css({
                            "background-color": "#ece9d8",
                            color: "#ccc",
                            border: "1px solid #CCDCEF"
                            });
                            $("#pub-btn0").addClass("new-pub-btn-valid").removeClass("new-pub-btn-unvalid").prop("disabled",false);
                        }
                        else {
                            $("#add-pub-loading0").css("display","none");
                            $("#add-pub-btn0").css("display","block");
                            $("#write-error-box0 .write-error-desc").html(ret.error).show();
                        }
                    },
                    error:function (arg) {
                        $("#add-pub-loading0").css("display","none");
                        $("#add-pub-btn0").css("display","block");
                        $("#write-error-box0 .write-error-desc").html("未知错误请重试").show();
                    }
                })
            };
        },
        //清空发布框的内容
        clearPublish:function () {
            switch(kind){
                case 0:
                    $("#add-pub-loading0").css("display","none");
                    $("#add-pub-btn0").css("display","block");
                    $("#txt-zixun-content").val("");
                    $("#txt-zhaiyao").val("");
                    $("#txt-zixun").val("").attr("disabled", !1).css({
                        "background-color": "#fff",
                        color: "#333"
                    });
                    $("#pub-btn0").addClass("new-pub-btn-unvalid").removeClass("new-pub-btn-valid").prop("disabled",true);
                    break;
                case 1:
                    $("#txt-duanzi").val("");
                    $("#pub-btn1").addClass("new-pub-btn-unvalid").removeClass("new-pub-btn-valid").prop("disabled",true);
                    break;
                case 2:
                    $("#upload-img").attr("src","");
                    $("#upload-img-area").show();
                    $("#show-img-area").hide();
                    $("#txt-img").val("");
                    $("#pub-btn2").addClass("new-pub-btn-unvalid").removeClass("new-pub-btn-valid").prop("disabled",true);
                    break;

            }
        },
        //发布内容包括资讯段子和图片
        publishSomeThing:function () {
            post_dict={};
            switch (kind){
                case 0:
                    $("#pub-btn0").css("display","none");
                    $("#pub-loading0").css("display","block");
                    post_dict["kind"]=0;
                    post_dict["link"]=$("#txt-zixun").val();
                    post_dict["title"]=$("#txt-zixun-content").val();
                    post_dict["zhaiyao"]=$("#txt-zhaiyao").val();
                    $.ajax({
                        url:"/chouti/publish/",
                        type:"post",
                        data:post_dict,
                        success:function (arg) {
                            chouti.hidePublishBox();
                            $("#pub-loading0").css("display","none");
                            $("#pub-btn0").css("display","block");
                            chouti.clearPublish();
                            location.reload();
                        },
                        error:function (arg) {

                        }
                    });
                    break;
                case 1:
                    $("#pub-btn1").css("display","none");
                    $("#pub-loading1").css("display","block");
                    post_dict["kind"]=1;
                    post_dict["zhaiyao"]=$("#txt-duanzi").val();
                    $.ajax({
                        url:"/chouti/publish/",
                        type:"post",
                        data:post_dict,
                        success:function (arg) {
                            chouti.hidePublishBox();
                            $("#pub-loading1").css("display","none");
                            $("#pub-btn1").css("display","block");
                            chouti.clearPublish();
                        },
                        error:function (arg) {

                        }
                    });
                    break;
                case 2:
                    $("#pub-btn2").css("display","none");
                    $("#pub-loading2").css("display","block");
                    post_dict["kind"]=2;
                    post_dict["zhaiyao"]=$("#txt-img").val();
                    post_dict["filelink"]=$("#upload-img").attr("src");
                    $.ajax({
                        url:"/chouti/publish/",
                        type:"post",
                        data:post_dict,
                        success:function (arg) {
                            chouti.hidePublishBox();
                            $("#pub-loading2").css("display","none");
                            $("#pub-btn2").css("display","block");
                            chouti.clearPublish();
                        },
                        error:function (arg) {

                        }
                    });
                    break;

            }
        },
        //点赞加1的动画效果，用了animate
        showDiggMove:function (e,n) {
            var i = $("<span></span>", {
                css: {
                    "font-weight": "bold",
                    color: "#4fc416",
                    "font-size": "20px",
                    position: "absolute",
                    "z-index": "6",
                    left: "25px",
                    top: $(n).parent().position().top + "px"
                }
            }).text("+1").appendTo(e);
            i.animate({top: "-=70", left: "+=3", "font-size": 60, opacity: 0}, 600, function () {
                i.remove()
            })
        },
        //点赞减1的动画效果,原理同上
        showLessMove:function (e,n) {
            var i = $("<span></span>", {
                css: {
                    "font-weight": "bold",
                    color: "#99AECB",
                    "font-size": "20px",
                    position: "absolute",
                    "z-index": "6",
                    left: "25px",
                    top: $(n).parent().position().top + "px"
                }
            }).text("-1").appendTo(e);
            i.animate({top: "-=70", left: "+=18", "font-size": 60, opacity: 0}, 600, function () {
                i.remove()
            })
        },
        //点赞按钮事件
        dianzanClick:function () {
            var t = $(this);
            var o = t.parent().parent().parent();
            //console.log("hi");
            //console.log(t);
            //console.log(o);
            //console.log(t.position());
            var newID = t.children("i").html();
            console.log(newID);
            var post_dict = {};
            post_dict["newID"]=newID;
            $.ajax({
                url:"/chouti/dianzan/",
                type:"post",
                data:post_dict,
                success:function (arg) {
                    var ret=JSON.parse(arg);
                    if(ret.status==true){
                        if(ret.data=="jiayi"){
                            chouti.showDiggMove(o,t);
                            t.removeClass();
                            t.addClass("isVoted");
                            t.children("span").addClass("vote-actived");
                            t.children("b").html(ret.count);
                        }
                        else {
                            chouti.showLessMove(o,t);
                            t.removeClass();
                            t.addClass("digg-a");
                            t.children("span").removeClass("vote-actived");
                            t.children("b").html(ret.count);
                        }
                    }
                    console.log(arg);

                },
                error:function (arg) {
                    console.log(arg);
                }
            });
            //chouti.showDiggMove(o,t);
        },
        //评论按钮事件
        commentClick: function (){
            var t = $(this);
            var newID = t.children("i").html();
            console.log(newID);
            var n = $("#comment-box-area-"+newID);
            if (!n.is(":hidden")){
                return void n.hide();
            }
            n.show().find("#loading-comment-top-"+newID).css({display:"inline"});
            $.ajax({
                url:'/chouti/getcomments/',
                type:'post',
                data:{newID:newID},
                success:function (arg) {
                    var ret = JSON.parse(arg);
                    if(ret.status==true){
                        console.log('get comments success');
                        $("#loading-comment-top-" + newID).hide();
                        $("#comment-list-top-" + newID).html(ret.data);
                        $("#comment-list-top-" + newID).show();
                        $("#huifu-top-box-"+ newID).css({display:"block"});
                    }
                    else {
                        console.log('get comments error');
                    }
                },
                error:function (arg) {

                }
            });
            $("comment-list-top-" + newID).html("");
        },
        getcommentBynewID:function (newID) {
              $.ajax({
                url:'/chouti/getcomments/',
                type:'post',
                data:{newID:newID},
                success:function (arg) {
                    var ret = JSON.parse(arg);
                    if(ret.status==true){
                        console.log('get comments success');
                        $("#comment-list-top-" + newID).html(ret.data);
                    }
                    else {
                        console.log('get comments error');
                    }
                },
                error:function (arg) {

                }
            });
        },
        huifuClick:function () {
            var newID = $(this).attr('news');
            var who = $(this).attr('who');
            console.log(newID);
            console.log(who);
            var comment = $("#txt-huifu-top-"+newID).val();
            $("#pub-btn-top-"+newID).hide();
            $("#pub-loading-top-"+newID).show();
            $.ajax({
                url:'/chouti/huifu/',
                type:'post',
                data:{newID:newID,who:who,comment:comment},
                success:function (arg) {
                    var ret = JSON.parse(arg);
                    if (ret.status==true){
                        $("#pub-btn-top-"+newID).show();
                        $("#pub-loading-top-"+newID).hide();
                        chouti.getcommentBynewID(newID);
                        console.log('huifu success!')
                    }
                    else {
                        $("#pub-btn-top-"+newID).show();
                        $("#pub-loading-top-"+newID).hide();
                        console.log('huifu fail!!')
                    }
                },
                error:function () {
                    $("#pub-btn-top-"+newID).show();
                    $("#pub-loading-top-"+newID).hide();
                    console.log('huifu fail!');
                }

            })

        },
        huifuInputStat:function () {
            var newID = $(this).attr('lang');
            var huifu = $(this).val();
            console.log(huifu);
            var e = chouti.clearBeforeNull(huifu);
            e = chouti.clearMidNull(e);
            console.log(e);
            for (var n = 0, i=0;i<e.length;i++){
                var o = e.charCodeAt(i);
                o>=1&&o<=126||65376<=o && o<=65439 ?n++:n+=2
            }
            var a = parseInt(n/2),s=n%2;
            0!=s && (a+=1);
            if (a!=0){
                $("#pub-btn-top-"+newID).removeClass('add-pub-btn-unvalid').addClass('add-pub-btn-valid');
                $("#pub-btn-top-"+newID).off('click');
                $("#pub-btn-top-"+newID).on('click',chouti.huifuClick);
            }
            else {
                $("#pub-btn-top-"+newID).removeClass('add-pub-btn-valid').addClass('add-pub-btn-unvalid');
                $("#pub-btn-top-"+newID).off('click');
            }

        },
        //绑定所有点赞,评论,收藏等相关操作
        bindAllNewsAction:function () {
            $("#content-list").on("click","a.digg-a",chouti.dianzanClick);
            $("#content-list").on("click","a.isVoted",chouti.dianzanClick);
            $("#content-list").on("click","a.discus-a",chouti.commentClick);
            $("#content-list").on("mouseenter","span.folder",function () {
                $(this).find("div.comment-line-top").css({display:'block'});
                $(this).addClass('hover');
            });
            $("#content-list").on("mouseleave","span.folder",function () {
                $(this).find("div.comment-line-top").css({display:'none'});
                $(this).removeClass('hover');
            });
            $("#content-list").on("click","a.huifu-a",function () {
               var newID = $(this).attr('linkid');
               var commentID = $(this).attr('lang');
               var nickName = $(this).attr('usernick');
               $("#nick--"+newID).html(nickName);
               $("#lab-comment-top-"+newID).css({display:'block'});
               $("#pub-btn-top-"+newID).attr('who',commentID);
            });
            $("#content-list").on("input propertychange","textarea.txt-huifu-top",chouti.huifuInputStat);
        }


    }
})(jQuery);