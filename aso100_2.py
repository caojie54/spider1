# -*- coding: utf-8 -*-
#!usr/bin/env python3
"""
Created on Fri Aug  4 15:53:12 2017

@author: caojie
"""

''' 	'''
import requests
import queue
from lxml import etree
import time
from get_proxies import ProxyPool
import os
import sys, io

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

to_crawl=queue.Queue()    #first in first out 
crawled= set()

main_url="https://aso100.com"


ua = {
      'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
      }

initial_url={}         # url   and category information 
ses=requests.Session() #init session
#just for aso100.com
def get_rank_url(url,cate_level=1,cate_info={},proxies={}):
    print("we will requests : "+url+", level is :"+str(cate_level)+",cate_info :  " +str(cate_info))
    #
    global ses
    a = requests.adapters.HTTPAdapter(max_retries=3)
    b = requests.adapters.HTTPAdapter(max_retries=3)
    ses.mount('http://', a)
    ses.mount('https://', b)
    #time.sleep(2)
    try:
        r = ses.get(url,headers=ua,proxies=proxies,timeout=10)
        
        print(r)
        #print(r.cookies)
        tree = etree.HTML(r.content)
        #get current url cate_level 
        cu_cate_level=len(tree.xpath("//div[@id='rank0']/div/ul/li[@class='dropdown']"))-1  #except date
        print("cu_cate_level is"+str(cu_cate_level))
        
        #generate new Session with proxy
        if cu_cate_level == -1:
            ses.close()
            proxypool = ProxyPool()
            proxies = proxypool.getproxy()
            new_ses = requests.Session()
            print("get new Session with new proxies:"+str(proxies))
            #new_ses.proxies = proxies
            ses = new_ses
            get_rank_url(url,cate_level,cate_info,proxies)
        else:
            if cate_level > cu_cate_level:
                initial_url[url]=cate_info
                # reduce request times,get data here
                get_data(r);
                #print(str(initial_url))
            else:
                cate_title=tree.xpath("//div[@id='rank0']/div/ul/li[@class='dropdown']["+str(cate_level)+"]/span/text()")[0]
            
                next_level_url_list = tree.xpath("//div[@id='rank0']/div/ul/li[@class='dropdown']["+str(cate_level)+"]/ul/li/a/@href")
                next_level_url_list_cate = tree.xpath("//div[@id='rank0']/div/ul/li[@class='dropdown']["+str(cate_level)+"]/ul/li/a/text()")
                cate_level = int(cate_level)+1
                for i in range(len(next_level_url_list)):
                    cate_info[cate_title]=next_level_url_list_cate[i]
                    #time.sleep(2)
                    get_rank_url(main_url+next_level_url_list[i],cate_level,cate_info,proxies)
    except requests.exceptions.ConnectionError as e:
            print("no response..........go on !",e)
            ses.close()
            proxypool = ProxyPool()
            proxies = proxypool.getproxy()
            new_ses = requests.Session()
            print("get new Session with new proxies:"+str(proxies))
            #new_ses.proxies = proxies
            ses = new_ses
            get_rank_url(url,cate_level,cate_info,proxies)
            
            
file_count=0
#get needed data
def get_data(response):
    global file_count
    file_count=file_count+1
    tree = etree.HTML(response.content)
    # rank data
    node = tree.xpath("//div[@class='row']/div/div/a/div/h5/text()")
    cate_info = initial_url[response.url]
    cate_info = str(cate_info)
    if os.path.exists("./aso100")== False:
        os.mkdir("./aso100")    
    file_name="./aso100/"+str(file_count)+".txt"
    with open(file_name,'w') as f:
        f.write(cate_info+"\n")
        for i in range(len(node)):
            f.write(node[i]+'\n')
    print("write file %s success" % file_name)
    
if __name__ =='__main__':
    get_rank_url("https://aso100.com/rank/marketRank/")
    
