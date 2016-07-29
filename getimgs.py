#encoding=utf8
import requests
from bs4 import BeautifulSoup
import os
import shutil

class getobj:
    def __init__(self):
        self.http=requests.Session()
        self.headers={"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
        #self.http.proxies = {'http': 'http://127.0.0.1:8080','https': 'http://127.0.0.1:8080'}
        self.page=1
        self.isfirst=True  #第一次下载图片的话,不能下载到原始图片
        self.postdata={
            "__VIEWSTATE":""
            ,"__EVENTTARGET":""
            ,"__EVENTARGUMENT":""
            ,"__EVENTVALIDATION":""
            ,"txtZJBH":""
            ,"txtActualProductName":""
            ,"txtCompanyTB":""
            ,"Hsort":""
            ,"Htable":""
        }
    def getParams(self,html):
        bs=BeautifulSoup(html)
        params=bs.select("#form1 input")
        for param in params:
            name=param.attrs.get('name')
            value=param.attrs.get('value')
            if(value==None):
                value=""
            if(name!='' and name!=None and name!="Button5"):
                self.postdata[name]=value
        self.postdata['__EVENTTARGET']='hp1'
        self.postdata['__EVENTARGUMENT']=self.page  #设置当前页面
    def step1(self):
        if(self.postdata['__VIEWSTATE']==""):
            print("init:page-params" )
            res=self.http.get("http://27.17.15.195:803/show/YPBJ.aspx",headers=self.headers)
            self.getParams(res.text)
    def step2(self):
        path="imgs/%d.png" % self.page
        if(os.path.isfile(path)):
            print("exist:img-%d" % self.page)
            self.page+=1
            return
        print("init:page-%d" % self.page)
        res=self.http.post("http://27.17.15.195:803/show/YPBJ.aspx",data=self.postdata,headers=self.headers)
        if(res.status_code!=200):
            return
        self.getParams(res.text)
        print("get:img-%d" % self.page)
        res=self.http.get("http://27.17.15.195:803/show/GridPic1.aspx",headers=self.headers)
        if(res.status_code==200):
            if(self.isfirst):
                self.isfirst=False
            else:
                f=open(path,"wb")
                f.write(res.content)
                f.close()
                self.page+=1

def movefile():
    for i in range(2,2996):
        source="imgs/%d.png" %i
        target="imgs/%d.png" % (i-1)
        shutil.move(source,target)


if __name__=="__main__":
    #movefile()
    #exit(0)
    obj=getobj()
    while obj.page<=2995:
        obj.step1()
        obj.step2()