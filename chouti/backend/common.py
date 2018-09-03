# -*- coding:utf-8 -*-
# Author:YEAR

import hashlib
import time
import random
import collections


def random_code():
    code = ''
    for i in range(4):
        current = random.randrange(0, 4)
        if current != i:
            temp = chr(random.randint(65, 90))
        else:
            temp = random.randint(0, 9)
        code += str(temp)
    return code


def generate_md5(value):
    r = "mika"
    obj = hashlib.md5(r.encode('utf-8'))
    obj.update(value.encode('utf-8'))
    return obj.hexdigest()


def generate_random_md5(value):
    r = str(time.time())
    obj = hashlib.md5(r.encode('utf-8'))
    obj.update(value.encode('utf-8'))
    return obj.hexdigest()


def isEmail(email):
    if email:
        return True
    else:
        return False


def tree_search(d_dic, comment_obj):
    for k, v_dic in d_dic.items():
        if k.id == comment_obj.replay_id:
            d_dic[k][comment_obj] = collections.OrderedDict()
            return
        else:
            tree_search(d_dic[k], comment_obj)


def build_tree(comment_list):
    comment_dic = collections.OrderedDict()

    for comment_obj in comment_list:
        if comment_obj.replay_id is None:
            comment_dic[comment_obj] = collections.OrderedDict()
        else:
            tree_search(comment_dic, comment_obj)

    return comment_dic

TEMP1 = """
    <li class="items" style='padding:8px 0 0 %spx;'>
        <span class='folder' id='comment_folder_%s'>
            <div class="comment-L comment-L-top">
                <a href="#" class="icons zhan-ico"></a>
                <a href="#" class="">
                    <img src="/statics/img/touxiang.jpg">
                </a>
            </div>
            <div class="comment-R comment-R-top" style="background-color: rgb(246, 246, 246);">
                <div class="pp">
                    <a class="name" href="#">%s</a>
                    <span class="p3">%s</span>
                    <span class="into-time into-time-top">%s</span>
                    <span class="into-time s-phone">来自<a class="phone-name" href="#" target="_blank">一加3T</a></span>
                </div>
                <div class="comment-line-top" style="display:none;" >
                    <div class="comment-state">
                        <a class="ding" lang="%s" href="javascript:;"><b>顶</b><span class="ding-num">[%s]</span></a>
                        <a class="cai" lang="%s" href="javascript:;"><b>踩</b><span class="cai-num">[%s]</span></a>
                        <span class="line-huifu">|</span>
                        <a class="see-a jubao" href="javascript:;" lang="%s" linkid="%s">举报</a>
                        <span class="line-huifu">|</span>
                        <a class="see-a huifu-a" href="javascript:;" id="huifuBtn%s" lang="%s" usernick="%s" linkid="%s">回复</a>
                        <input type="hidden" id="hid%s" value="%s">
                    </div>
                </div>
            </div>
        </span>
    """

def generate_comment_html(sub_comment_dic,margin_left_val):
    html=""
    for k,v in sub_comment_dic.items():
        html += "<ul style='background: url('/statics/img/pinglun_line.gif') 0px -10px no-repeat scroll transparent; display: block;' >"
        html += TEMP1 %(margin_left_val,k.id,k.userinfo.username,k.content,k.ctime,k.id,k.up,k.id,k.down,k.id,k.news_id,k.id,k.id,k.userinfo.username,k.news_id,k.id,k.id)
        html += generate_comment_html(v,16)
        html += "</li>"
        html += "</ul>"

    return html

def tree_html(comment_dic):
    treeHtml=''
    for k, v in comment_dic.items():
        treeHtml += TEMP1 %(0,k[0],k[3],k[1],k[4],k[0],k[5],k[0],k[6],k[0],k[7],k[0],k[0],k[3],k[7],k[0],k[0])
        treeHtml += generate_comment_html(v,16)
        treeHtml += "</li>"
    return treeHtml


if __name__ == "__main__":
    print('test start')
    t = random_code()
    print(t)
    print(generate_md5('year93926'))
