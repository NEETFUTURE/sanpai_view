# -*- coding: utf_8 -*-
from urllib import request
import sys
import lxml.html
import os.path
import pickle

from bottle import template
from bottle import route, run
from fractions import Fraction


URL = "http://thewaterducts.sakura.ne.jp"
PHPU = "/php/waterducts/imta"
DATABASE = os.path.join(os.path.curdir, "data.pickle")
gData = None

def getlist(num):
    r=request.urlopen(URL+"/php/waterducts/imta/?log=%d"%(num))
    root = lxml.html.fromstring(r.read().decode("cp932"))

    a = root.xpath("//td[@class='title']")
    sclist = [dict(id = b.xpath("../td")[0].text.strip(),\
                   title = b.xpath("a")[0].text.strip(),\
                   url = URL+PHPU+b.xpath("a")[0].attrib['href'].strip()[1:],\
                   author = b.xpath("../td")[2].text.strip(),\
                   hyoka = b.xpath("../td")[5].text.strip(),\
                   point = b.xpath("../td")[6].text.strip(),\
                   rate = b.xpath("../td")[7].text.strip(),\
                   size = b.xpath("../td")[8].text.strip(),\
                   ) 
                   for b in a]
    sclist = [[b, dict(hyoka = float(Fraction_zero(b["hyoka"])),
                       point = int(b["point"]),
                       rate = float(b["rate"]),
                       size = float(b["size"].rstrip("KB "))
                       )
             ] for b in sclist]

    return sclist

def getclists():
    tpc = request.urlopen(URL + "/php/waterducts/imta")
    ro = lxml.html.fromstring(tpc.read().decode("cp932"))
    links = ro.xpath("//div[@class='page']/ul/li")

    print("リンクの数: %d"%(len(links)))

    clist = []
    for i in range(len(links)):
        clist.extend(getlist(i))
    return clist



@route('/')
@route('/index')
def base():
    return template('templates/cate.html', clists = gData)

@route('/sort_hyoka')
def sort_hyoka():
    cli = sorted(gData, key=lambda x: x[1]["hyoka"], reverse=True)
    return template('templates/cate.html', clists = cli)

def Fraction_zero(n):
    try:
        ans = Fraction(n)
    except ZeroDivisionError:
        return 0.0
    return float(ans)


if __name__ == '__main__':
    if(not os.path.isfile(DATABASE)):
        print("save data")
        gData = getclists()
        with open(DATABASE, 'wb') as f:
            pickle.dump(gData,f)
    else:
        print("read data")
        with open(DATABASE, 'rb') as f:
            gData = pickle.load(f)

    run(host='0.0.0.0', port=80,debug=False, reloader=True)
