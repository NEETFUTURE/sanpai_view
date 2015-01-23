# -*- coding: utf_8 -*-
import requests
import sys
import lxml.html
import sqlite3
import os.path
from bottle import template
from bottle import route, run


URL = "http://thewaterducts.sakura.ne.jp"
PHPU = "/php/waterducts/imta"
DATABASE = "data.db"

def getlist(num):
    r=requests.get(URL+"/php/waterducts/imta/?log=%d"%(num))
    root = lxml.html.fromstring(r.text)

    a = root.xpath("//td[@class='title']")
    sclist = [dict(id       = b.xpath("../td")[0].text.strip(),\
                   title    = b.xpath("a")[0].text.strip(),\
                   url      = URL+PHPU+b.xpath("a")[0].attrib['href'].strip()[1:],\
                   author   = b.xpath("../td")[2].text.strip(),\
                   hyoka    = b.xpath("../td")[5].text.strip(),\
                   point    = b.xpath("../td")[6].text.strip(),\
                   rate     = b.xpath("../td")[7].text.strip(),\
                   size     = b.xpath("../td")[8].text.strip(),\
                   ) for b in a]

    return sclist

def getclists():
    top_page_ct = requests.get(URL + "/php/waterducts/imta")
    ro = lxml.html.fromstring(top_page_ct.text)
    links = ro.xpath("//div[@class='page']/ul/li")

    print("リンクの数: %d"%(len(links)))

    clist = []
    for i in range(len(links)):
        clist.extend(getlist(i))
    return clist


@route('/')
@route('/index')
def base():
    clists = getclists()
    return template('templates/cate.html', clists = clists)

run(host='localhost', port=8080,debug=True, reloader=True)
