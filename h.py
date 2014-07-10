#!/usr/bin/python
# -*- coding: utf-8 -*-  

from bs4 import BeautifulSoup
import urllib, re
import sys, urllib2  
import logging
import time 
import operator

reload(sys)
sys.setdefaultencoding( "utf-8")

logger=logging.getLogger()
string = time.strftime("%Y-%m-%d")
handler=logging.FileHandler("log/log" + string + ".txt")
logger.addHandler(handler)

logger.setLevel(logging.NOTSET)


class my_list(list):
    def __init__(self):
        list.__init__(self)
            
    def __str__(self):
        return "%s" % ",".join(self)

class Hlitem:
    link = ""
    room = ""
    area = ""
    price = ""
    desc = ""
    def __init__(self,a,b,c,d,e):
        self.link = a
        self.room = b
        self.area = c
        self.price = d
        self.desc = e
    def show(self):
        print self.link
        print self.room
        print self.area
        print self.price
        print self.desc
    def __getitem__(self, key):
        if ( key == 0):
            return self.link
        if ( key == 1):
            return self.room
        if ( key == 2):
            return self.area
        if ( key == 3):
            return self.price
        if ( key == 4):
            return self.desc
        return self.link
        

def hll(item):
    pp = ""
    p = ""
    hll_pattern = re.compile('<a href="(http\S*)" target')
    for item1 in item.find_all('a'):
        item1 = item1.__str__()
        a = hll_pattern.match(item1)
        if a:
            b =  a.group(1)
            break
#    la.append(b)
    i2 = item.find('li', attrs={"class":"two"})
    i3 = item.find('li', attrs={"class":"three"})
    price = item.find('div', attrs={"class":"price"})
    for tt in price.text.strip().splitlines():
        tt=tt.rstrip()
        pp=pp+tt
    desc = item.find('h3')
    for t in desc.text.strip().splitlines():
        t=t.rstrip()
        p=p+t
    a = Hlitem(b, i2.text, i3.text, pp, p) 
    return a
'''
#debug info
    print i2.text.strip()
    print i3.text.strip()
    print "123"
    print price.text.strip()
    print "234"
    print desc.text.strip()
    print "345"
    print pp
    print "456"
    print p
    print "567"
    raw_input()
'''
'''
    la.append(i2.text.strip())
    la.append(i3.text.strip())
    la.append(price.text.strip())
    la.append(desc.text.strip())
    return la
'''
    
    
def hl_openpage(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    html = response.read()  
    soup = BeautifulSoup(html)
#   soup = soup.prettify()
    return (html, soup)

def hl_gethousenum(html):
    page_pattern = re.compile('<span>(\d*)</span>套在售房源')
    page_result = page_pattern.search(html)
    if page_result:
        return int(page_result.group(1))
    
def hl_getHlitems(soup):
    les = soup.find("div", id="listData")
    la = []
    i = 0
    for item in les:
        i=i+1
        if item:
            if i % 2 == 0:
                logger.info("i = %d", i)
                logger.info(item)
                a = hll(item)
                la.append(a) 
    return la



def searchzone(searchstring):
    url1 = 'http://beijing.homelink.com.cn/ershoufang/rs'+searchstring+'/'

    html,soup = hl_openpage(url1)
#    myfile = file("p1.html", 'w')
#    print >> myfile, html
#    myfile.close()

    hl_houseNum = hl_gethousenum(html)

    hl_itemlist = hl_getHlitems(soup)
#    printzonedata(hl_itemlist)
#    raw_input()
    hl_pageNum = hl_houseNum / len(hl_itemlist) 
    if ((hl_houseNum % len(hl_itemlist)) != 0):
        hl_pageNum += 1

    for i in range(2, hl_pageNum + 1):
        url2 = 'http://beijing.homelink.com.cn/ershoufang/pg'+str(i)+'rs'+searchstring
#       print url2
        html,soup = hl_openpage(url2)
#        myfile = file("p2.html", 'w')
#        print >> myfile, html
#        myfile.close()
        a = hl_getHlitems(soup)
        hl_itemlist += a
#    print "add 2nd page\n"
#    printzonedata(hl_itemlist)
#    raw_input()
    hl_itemlist.sort(key=operator.itemgetter(0))
#    print "item sorted\n"
#    printzonedata(hl_itemlist)
#    raw_input()
    return hl_itemlist

def printzonedata(il):
    for i in range(len(il)):
        print i + 1
        il[i].show()
        print "\n"

zonelist2 = [
    "龙泽苑东区",
]

zonelist = [
    "嘉铭桐城A区",
    "嘉铭桐城B区",
    "嘉铭桐城C区",
    "嘉铭桐城D区",
    "嘉铭桐城E区",
    "嘉铭桐城F区",
    "鹿港嘉苑", 
    "远洋万和城A区",
    "远洋万和城B区",
    "远洋万和城C区",
    "方舟苑一期",
    "方舟苑二期",
    "方舟苑三期",
    "大西洋新城A区",
    "大西洋新城B区",
    "大西洋新城C区",
    "大西洋新城D区",
    "大西洋新城E区",
    "大西洋新城F区",
    "大西洋新城G区",
]

def main():
    string = time.strftime("%Y-%m-%d-%H-%M")
    fs = "./fang/fang"+string+".txt"
    f=open(fs,'w')
    saveout = sys.stdout
    sys.stdout=f 

    for ss in zonelist:
        hl_itemlist = searchzone(ss)
        print "********************"+ss+"********************\n"
        printzonedata(hl_itemlist)
    sys.stdout = saveout
    f.close()
    
if __name__ == '__main__':
    main()

