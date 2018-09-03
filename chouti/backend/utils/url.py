# -*- coding:utf-8 -*-
# Author:YEAR

import chardet
from urllib import request
from lxml import etree
from bs4 import BeautifulSoup

def utf8_transfer(str):
    '''
    转换成utf8编码
    :param str:需要转换的字符串
    :return:转换后的字符串
    '''
    try:
        #print(chardet.detect(str)["encoding"])
        if chardet.detect(str)["encoding"]=="GB2312":
            str=str.decode("GB2312","ignore").encode("utf-8")
        elif chardet.detect(str)["encoding"]=="utf-8":
            str=str.decode("utf-8","ignore").encode("utf-8")
    except Exception as e:
        print("utf8_transfer error",str,e)
    return str

def get_title_xpath(html):
    '''
    用xpath抽取网页的标题
    :param html: 网页的html代码
    :return: 网页的标题
    '''
    html=utf8_transfer(html)
    htmlEncoding=chardet.detect(html)["encoding"]
    page=etree.HTML(html,parser=etree.HTMLParser(encoding=htmlEncoding))
    title = page.xpath('/html/head/title/text()')
    try:
        title=title[0].strip()
    except IndexError:
        print("Nothing")
    return title

def get_title_bs(html):
    '''
    用beautifulsoup4获取网页的标题
    :param html: 网页的html代码
    :return: 网页的标题
    '''
    html=utf8_transfer(html)
    soup=BeautifulSoup(html,'lxml')
    return soup.title.string

def get_description_bs(html):
    '''
    用beautifulsoup4获取网页的描述
    :param html: 网页的html代码
    :return: 网页的描述
    '''
    html=utf8_transfer(html)
    soup=BeautifulSoup(html,'lxml')
    try:
        desc=soup.find(attrs={"name":"description"})["content"]
    except Exception as e:
        print("get_description_bs error",e)
        desc="No Description."
    return desc
if __name__=="__main__":
    url="http://www.baidu.com/"
    html=request.urlopen(url).read()
    #print(html.decode("utf-8","ignore"))
    print("xpath",get_title_xpath(html))
    print("bs4", get_title_bs(html))
    print("bs4 desc",get_description_bs(html))
    #print(html)


