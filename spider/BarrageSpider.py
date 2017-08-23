#coding = utf-8

import re
import requests
import logging 
import json
import sys
import io


class BarrageSpider():

    def __init__(self):
        
        self.start_urls=[]
        self.cate_id=[32,35,153]
        self.pagesize=50 
        self.time_from=20170810 
        self.time_to=20170820
        
    
    def buildStartURLs(self):
        for id in self.cate_id:
            url_str="https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&pic_size=160x100&order=click&copy_right=-1&cate_id={cate_id}&page=1&pagesize={pagesize}&time_from={time_from}&time_to={time_to}"
            start_url=url_str.format(cate_id=str(id),pagesize=self.pagesize,time_from=self.time_from,time_to=self.time_to)
            self.start_urls.append(start_url)
         
    def getCID(self,url):
        
        page=requests.get(url).text
        try :
            cid=re.findall('cid\=(\d+?)\&aid=(\d+?)\&pre_ad\=',page)[0][0]
        except IndexError:
            cid =None
            pass
        logging.info("cid is \t%s",cid)
        print(cid)

        return cid
    def getAidURLs(self,api_url):
        
        response=requests.get(api_url)
        data=json.loads(response.text)
        urls=[]
        
        for  item in data['result']:
            urls.append(item['arcurl'])
                
        return urls

    def downloadBarrage(self,url,cid):
        xml_content = requests.get(url).text 
#         sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
#         print(xml_content)
        res=self.processXML(xml_content)
#         print(res)
        with open("D:/Barrage/"+str(cid)+".txt", "w+",encoding='utf-8') as code:
            for s in res:
                code.write(','.join(s)+'\n')
    
    def run(self):
        self.buildStartURLs()
        for start_url in self.start_urls:
            print("startURL"+start_url)
            urls=self.getAidURLs(start_url)
            print(len(urls))
            for url in urls:
                cid=self.getCID(url)
                if cid:
                    res_url="http://comment.bilibili.com/"+str(cid)+".xml"
                    self.downloadBarrage(res_url,cid)

    def processXML(self,xml_content):
        xml_content=xml_content.replace("\r\n","")
        list_s=re.findall('<d p="(.+?)">(.+?)</d>', xml_content)
        return list_s
    
        
if __name__=="__main__":
    a=BarrageSpider()
    a.run()
    
    
    