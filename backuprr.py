#!/usr/bin/env python
#encoding=utf-8
import os
import sys
import re
import urllib2
import urllib
import cookielib
import lxml.html
import time
import platform
import getpass
import _elementpath as DONTUSE

class Renren(object):
   
    def __init__(self):
        self.name = self.pwd = self.content = self.domain = self.origURL =  ''
        self.operate = ''
        self.cj = cookielib.LWPCookieJar()
        self.ursid = 0
        self.dir = "./blogs/"
        self.count = 0
        try: 
            self.cj.revert('renren.coockie') 
        except Exception,e:
            pass
           
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
        urllib2.install_opener(self.opener)
   
   
    def setinfo(self,username,password,domain,origURL,blogdir='./blogs/'):

        self.name = username
        self.pwd = password
        self.domain = domain
        self.origURL = origURL
        self.dir = blogdir

    def login(self):

        params = {'domain':self.domain,'origURL':self.origURL,'email':self.name, 'password':self.pwd}
        print 'login.......'
        req = urllib2.Request( 
            'http://www.renren.com/PLogin.do', 
            urllib.urlencode(params) 
        )
       
        self.operate = self.opener.open(req)
        usrid = self.operate.geturl().split("http://www.renren.com/")[1]
        try:
            self.usrid = int(usrid)
        except:
            self.usrid = 0
        if self.usrid:
            print 'Logged on successfully!'
            self.cj.save('renren.coockie')
            self.start()
        else:
            print 'Logged on error\n'+self.operate.geturl()
   
    def start(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        print "Please input your latest blog's url:"
        firstblog = sys.stdin.readline()[:-1]
        print "Your latest blog's url is %s" % firstblog
        print "Begin to backup your blogs ..."
        while firstblog != None:
            firstblog = self.backupblog(firstblog)
            self.count += 1
            print "%s blogs backuped .." % self.count
            time.sleep(1)
        print "Backup finished ! %s blogs found !\nPress Enter to exit!" %self.count
        wait = sys.stdin.readline()[:-1]

      
    def backupblog(self, url):

        req = urllib2.Request(url)
        try:
            self.operate = self.opener.open(req)
        except:
            print "Blog: %s downloading error! please check the url!" % url
        infocontent = self.operate.read()
        #print infocontent
        html = lxml.html.fromstring(infocontent.decode('utf8'))
        next = html.xpath('//span[@class="float-right"]/a')
        if len(next) != 0:
            nexturl = next[0].get('href')
        else:
            nexturl = None
        times = html.xpath('//span[@class="timestamp"]')
        if len(times) != 0:
            pubtime = times[0].text.strip().replace(':','-')
        else:
            pubtime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
        titles = html.xpath('//h3[@class="title-article"]/strong')
        if len(titles) != 0:
            if platform.system() == "Windows":
                title = titles[0].text.strip().encode("gbk",'ignore')
                title = title.replace('\\','').replace(':','').replace('/','').replace('?','').replace('*','').replace('<','').replace('|','').replace('>','').replace('"','')
            else:
                title = titles[0].text.strip()
        else:
            title = "unkowntitle"

        fd = open(self.dir + pubtime + '----' + title + '.html', 'a+')
        fd.write(infocontent)
        fd.close()

        return nexturl

ren = Renren()
print "Instruction: please use your computer which logins renren frequently !"
print "Because this program doesn't recognise the validation code."
print "Any wrong input will lead to exit ! please be careful !"
time.sleep(5)
print "Please input your renren username such as abc@cnn.com :"
username = sys.stdin.readline()[:-1].strip()
print "Please input your renren password, it will be hidden for your safe while inputting:"
password = getpass.getpass('password:')
domain = 'renren.com'
origURL = 'http://www.renren.com/Home.do'
ren.setinfo(username,password,domain,origURL)
ren.login()

